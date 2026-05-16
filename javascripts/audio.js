/* Strands OmniVoice — one-click audio cards.
 *
 * Any element with class `so-audio` and a `data-src` attribute becomes an
 * inline player. Only one card plays at a time globally.
 *
 * Path resolution: data-src is normalised to point at the site-root
 * `assets/audio/<file>` regardless of how the markdown wrote it.
 *
 * Markdown can use any of:
 *   - "assets/audio/foo.mp3"        (works on /index.html)
 *   - "../assets/audio/foo.mp3"     (works at /a/page/)
 *   - "../../assets/audio/foo.mp3"  (works at /a/b/page/)
 *   - "/strands-omnivoice/assets/audio/foo.mp3" (gh-pages absolute)
 *
 * We strip leading `../` and `./` and resolve against site root (derived
 * from <link rel="canonical">), so all four forms become a working URL.
 */
(function () {
  'use strict';

  const PLAY_SVG  = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
  const PAUSE_SVG = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 5h4v14H6zm8 0h4v14h-4z"/></svg>';
  const EQ_SVG    = '<span class="so-eq"><span></span><span></span><span></span><span></span></span>';

  let activeAudio = null;
  let activeCard = null;

  /**
   * Find the absolute site root URL (origin + path-prefix) by comparing the
   * canonical URL with the current pathname. Works for both local dev (root
   * "/") and gh-pages (root "/strands-omnivoice/").
   *
   * Returns a string ending in "/".
   */
  function siteRoot() {
    const canon = document.querySelector('link[rel="canonical"]');
    let canonHref = canon && canon.href;
    let canonPath, here;

    if (canonHref) {
      try {
        canonPath = new URL(canonHref).pathname; // e.g. /strands-omnivoice/guide/voice-design/
      } catch (e) {
        canonHref = null;
      }
    }
    here = window.location.pathname; // e.g. /strands-omnivoice/guide/voice-design/

    // Use canonPath as authoritative if available (it always reflects mkdocs's
    // intended path, even if the user landed via redirect or alias).
    const path = (canonPath || here).replace(/index\.html$/, '');

    // Walk up the path until we find a known marker. mkdocs nav pages live
    // ≥ 1 segment below site root. We can't know how deep without help, so
    // we use a different trick: we know the page slug is the last directory
    // segment, AND the canonical url's directory IS the page directory.
    // Therefore site root = canonical's directory minus N segments, where N
    // is the number of path segments in `here` after removing leading slash
    // and trailing slash.
    //
    // Actually simplest portable rule: the relative URL `<base>` Material
    // bakes in is correct — it's exposed as the location of the canonical
    // link's directory minus the page's relative slug. We compute that by
    // resolving "" (empty href) relative to document.baseURI:
    //   document.baseURI for /strands-omnivoice/guide/voice-design/ → that URL itself
    // We need the SITE root, not the page directory. We get it by taking
    // `canonPath`, then removing trailing path segments equal to the page's
    // own depth in nav. But mkdocs encodes nav depth in the doc — we don't
    // know it from JS.
    //
    // Cleanest answer: each page bakes a <link rel="canonical"> pointing to
    // its own absolute URL. The number of "/" segments after site root in
    // canonPath equals the number of "/" segments in here after site root
    // (they are equal). So:
    //
    //   siteRoot = origin + (canonPath stripped of trailing "/N segments matching nav depth")
    //
    // We can't know nav depth, but we CAN compare canonPath with here and
    // find the longest common SUFFIX. siteRoot is canonPath minus that suffix.
    // Since canonPath and here usually match exactly, the common suffix IS
    // the entire path → siteRoot becomes empty. Wrong.
    //
    // The fundamental issue: canonical doesn't tell us where site root is.
    //
    // ── Final approach: read the absolute URL of one of mkdocs's CSS files ──
    // mkdocs always emits link tags like:
    //   <link rel="stylesheet" href="../../assets/stylesheets/main.xxx.css">
    // Resolved as absolute href, this points at the site root + assets/...
    // We use that to back out the site root.

    const cssLink = document.querySelector('link[rel="stylesheet"][href*="/assets/stylesheets/"]');
    if (cssLink && cssLink.href) {
      try {
        const u = new URL(cssLink.href);
        const idx = u.pathname.indexOf('/assets/stylesheets/');
        if (idx !== -1) {
          return u.origin + u.pathname.slice(0, idx + 1);
        }
      } catch (e) { /* ignore */ }
    }

    // Fallback: <base href> if Material set it, or origin + "/"
    const baseEl = document.querySelector('base[href]');
    if (baseEl && baseEl.href) {
      try {
        const u = new URL(baseEl.href);
        return u.origin + (u.pathname.endsWith('/') ? u.pathname : u.pathname + '/');
      } catch (e) { /* ignore */ }
    }

    return window.location.origin + '/';
  }

  /** Resolve any kind of `data-src` to an absolute URL. */
  function resolveSrc(raw) {
    if (!raw) return raw;
    // Already absolute or protocol-relative → leave it
    if (/^([a-z]+:)?\/\//i.test(raw)) return raw;
    // Already root-relative → leave it
    if (raw.startsWith('/')) return raw;

    // Strip leading `../` and `./` segments
    const cleaned = raw.replace(/^(\.\.\/)+/, '').replace(/^\.\//, '');
    return siteRoot() + cleaned;
  }

  function fmt(t) {
    if (!isFinite(t) || t < 0) return "0:00";
    const m = Math.floor(t / 60);
    const s = Math.floor(t % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  }

  function setIcon(card, playing) {
    const btn = card.querySelector(".so-audio-btn");
    if (btn) btn.innerHTML = playing ? PAUSE_SVG : PLAY_SVG;
    const tagSpot = card.querySelector(".so-audio-eq");
    if (tagSpot) tagSpot.innerHTML = playing ? EQ_SVG : "";
    card.classList.toggle("is-playing", playing);
  }

  function stopActive() {
    if (activeAudio) {
      try { activeAudio.pause(); } catch (e) {}
      if (activeCard) setIcon(activeCard, false);
    }
    activeAudio = null;
    activeCard  = null;
  }

  function attach(card) {
    if (card.dataset.soBound === "1") return;
    card.dataset.soBound = "1";

    const rawSrc = card.dataset.src;
    if (!rawSrc) return;
    const src = resolveSrc(rawSrc);

    if (!card.querySelector(".so-audio-btn")) {
      card.innerHTML = `
        <button class="so-audio-btn" type="button" aria-label="Play sample"></button>
        <div class="so-audio-body">
          <div class="so-audio-label">
            <span class="so-audio-title">${card.dataset.label || "Sample"}</span>
            ${card.dataset.tag ? `<span class="so-tag">${card.dataset.tag}</span>` : ""}
            <span class="so-audio-eq" aria-hidden="true"></span>
          </div>
          ${card.dataset.text ? `<div class="so-audio-text">${card.dataset.text}</div>` : ""}
          <div class="so-audio-track" role="progressbar"></div>
          <div class="so-audio-meta">
            <span class="so-audio-time">0:00</span>
            <span class="so-audio-dur">${card.dataset.duration ? card.dataset.duration + "s" : ""}</span>
          </div>
        </div>
      `;
    }

    const track = card.querySelector(".so-audio-track");
    const time  = card.querySelector(".so-audio-time");
    const dur   = card.querySelector(".so-audio-dur");
    const btn   = card.querySelector(".so-audio-btn");

    setIcon(card, false);

    const audio = new Audio();
    audio.preload = "none";
    audio.src = src;

    audio.addEventListener("loadedmetadata", () => {
      if (dur) dur.textContent = fmt(audio.duration);
    });

    audio.addEventListener("timeupdate", () => {
      const pct = audio.duration ? (audio.currentTime / audio.duration) * 100 : 0;
      card.style.setProperty("--p", pct + "%");
      if (time) time.textContent = fmt(audio.currentTime);
    });

    audio.addEventListener("ended", () => {
      setIcon(card, false);
      card.style.setProperty("--p", "0%");
      if (time) time.textContent = "0:00";
      if (activeCard === card) { activeAudio = null; activeCard = null; }
    });

    audio.addEventListener("error", () => {
      setIcon(card, false);
      const err = card.querySelector(".so-audio-text");
      if (err) err.textContent = "❌ failed to load: " + src;
    });

    function toggle() {
      if (audio.paused) {
        if (activeAudio && activeAudio !== audio) stopActive();
        audio.play().then(() => {
          activeAudio = audio;
          activeCard  = card;
          setIcon(card, true);
        }).catch(err => console.error("audio play failed", err));
      } else {
        audio.pause();
        setIcon(card, false);
        if (activeCard === card) { activeAudio = null; activeCard = null; }
      }
    }

    btn.addEventListener("click", toggle);
    if (track) track.addEventListener("click", (e) => {
      if (!audio.duration) return;
      const rect = track.getBoundingClientRect();
      const ratio = (e.clientX - rect.left) / rect.width;
      audio.currentTime = Math.max(0, Math.min(1, ratio)) * audio.duration;
    });
  }

  function scan() {
    document.querySelectorAll(".so-audio[data-src]").forEach(attach);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
  } else {
    scan();
  }

  if (typeof window !== "undefined" && window.document$) {
    window.document$.subscribe(scan);
  } else {
    new MutationObserver((muts) => {
      for (const m of muts) {
        if (m.addedNodes && m.addedNodes.length) { scan(); break; }
      }
    }).observe(document.body, { childList: true, subtree: true });
  }

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stopActive();
  });

  // Expose for debugging
  window.__soAudioResolve = resolveSrc;
  window.__soAudioRoot    = siteRoot;
})();
