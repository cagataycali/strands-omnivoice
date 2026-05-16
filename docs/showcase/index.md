---
hide:
  - toc
---

# 🌍 The 646-language showcase

<p class="so-intro">Every language OmniVoice supports — speaking the same line about <code>strands-omnivoice</code>, generated locally on Apple Silicon.</p>

<div class="so-stats" markdown>
<div class="so-stat"><span class="v" id="sc-total">646</span><span class="k">Languages</span></div>
<div class="so-stat"><span class="v" id="sc-native">30+</span><span class="k">Native scripts</span></div>
<div class="so-stat"><span class="v" id="sc-hours">581k</span><span class="k">Training hours</span></div>
<div class="so-stat"><span class="v" id="sc-rtf">~0.5</span><span class="k">RTF on M-series</span></div>
</div>

!!! tip "What you're hearing"
    Each clip says: *"Strands OmniVoice gives your agent a voice in over six hundred languages, with zero training data."*
    For ~30 major languages the line was translated and synthesized in-script (marked **native**); the rest use the English line with the matching language ID, letting OmniVoice apply that language's phonetic prior.

<div class="sc-controls">
  <input id="sc-search" type="search" placeholder="🔎 Search by language name or ISO code (e.g. 'Yoruba' or 'yor')..." autocomplete="off">
  <select id="sc-sort">
    <option value="num">Sort: official order</option>
    <option value="name">Sort: A → Z</option>
    <option value="hours">Sort: most training data</option>
    <option value="native">Sort: native first</option>
  </select>
  <span id="sc-count" class="sc-count"></span>
</div>

<div id="sc-grid" class="sc-grid">
  <div class="sc-loading">Loading 646 languages…</div>
</div>

<script>
(function(){
  const grid = document.getElementById('sc-grid');
  const search = document.getElementById('sc-search');
  const sort = document.getElementById('sc-sort');
  const countEl = document.getElementById('sc-count');

  let DATA = [];
  let viewIdx = 0;
  const PAGE_SIZE = 60;
  let filtered = [];

  // Lazy-load audio: only set src on play
  function makeCard(item, idx) {
    const el = document.createElement('div');
    el.className = 'sc-card' + (item.native ? ' sc-native' : '');
    el.innerHTML = `
      <div class="sc-head">
        <span class="sc-num">${String(idx).padStart(3,'0')}</span>
        <span class="sc-name">${item.name}</span>
        <span class="sc-id">${item.id}</span>
      </div>
      <div class="sc-meta">
        <span title="Training hours">📊 ${item.hours}h</span>
        <span title="Audio length">⏱ ${item.dur.toFixed(1)}s</span>
        ${item.native ? '<span class="sc-badge">native</span>' : ''}
      </div>
      <audio preload="none" controls>
        <source src="audio/${item.path}" type="audio/ogg; codecs=opus">
        Your browser does not support the audio element.
      </audio>
    `;
    return el;
  }

  function render(reset = true) {
    if (reset) {
      grid.innerHTML = '';
      viewIdx = 0;
    }
    const slice = filtered.slice(viewIdx, viewIdx + PAGE_SIZE);
    slice.forEach((item) => grid.appendChild(makeCard(item, item._idx)));
    viewIdx += slice.length;
    countEl.textContent = `${filtered.length} languages · showing ${Math.min(viewIdx, filtered.length)}`;
    if (viewIdx < filtered.length) {
      const more = document.createElement('button');
      more.className = 'sc-more';
      more.textContent = `Load next ${Math.min(PAGE_SIZE, filtered.length - viewIdx)}`;
      more.onclick = () => { more.remove(); render(false); };
      grid.appendChild(more);
    }
  }

  function applyFilter() {
    const q = (search.value || '').toLowerCase().trim();
    filtered = !q ? DATA.slice() : DATA.filter(d =>
      d.name.toLowerCase().includes(q) || d.id.toLowerCase().includes(q)
    );
    const sortKey = sort.value;
    if (sortKey === 'name') filtered.sort((a,b) => a.name.localeCompare(b.name));
    else if (sortKey === 'hours') filtered.sort((a,b) => b.hours - a.hours);
    else if (sortKey === 'native') filtered.sort((a,b) => (b.native?1:0) - (a.native?1:0));
    else filtered.sort((a,b) => a._idx - b._idx);
    render(true);
  }

  fetch('manifest.json').then(r => r.json()).then(j => {
    DATA = j.ok.map((d, i) => ({...d, _idx: i+1}));
    document.getElementById('sc-total').textContent = DATA.length;
    document.getElementById('sc-native').textContent = DATA.filter(d => d.native).length;
    applyFilter();
  }).catch(e => {
    grid.innerHTML = `<div class="sc-loading">Failed to load manifest: ${e.message}</div>`;
  });

  search.addEventListener('input', applyFilter);
  sort.addEventListener('change', applyFilter);
})();
</script>
