"""Generate the voice samples used in the docs site.

Run from repo root:

    python scripts/generate_doc_audio.py

Outputs WAVs under docs/assets/audio/ and (if `ffmpeg` is on PATH) MP3 mirrors
for cheaper page loads.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from strands_omnivoice.tools.clone import omnivoice_clone  # noqa: E402
from strands_omnivoice.tools.design import omnivoice_design  # noqa: E402
from strands_omnivoice.tools.model_lifecycle import omnivoice_load_model  # noqa: E402
from strands_omnivoice.tools.tts import omnivoice_tts  # noqa: E402

OUT = ROOT / "docs" / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

# ── Demo manifest ───────────────────────────────────────────────────────
SAMPLES = [
    {
        "id": "hello_auto",
        "tool": "tts",
        "label": "Auto voice · English",
        "tag": "tts",
        "args": dict(
            text="Hello world, welcome to Strands OmniVoice — multilingual zero-shot text to speech.",
            language="English",
            num_step=24,
        ),
    },
    {
        "id": "design_uk_elderly",
        "tool": "design",
        "label": "british elderly female",
        "tag": "design",
        "args": dict(
            text="Once upon a time, in a land far far away, there lived a wise old story-teller.",
            instruct="female, elderly, low pitch, british accent",
            language="English",
            num_step=24,
        ),
    },
    {
        "id": "design_us_male",
        "tool": "design",
        "label": "american middle-aged male",
        "tag": "design",
        "args": dict(
            text="Houston, we have a problem. Repeat — Houston, we have a problem.",
            instruct="male, middle-aged, american accent",
            language="English",
            num_step=24,
        ),
    },
    {
        "id": "design_whisper",
        "tool": "design",
        "label": "young whisper",
        "tag": "design",
        "args": dict(
            text="And then, when no one was watching, everything went silent.",
            instruct="female, young adult, whisper",
            language="English",
            num_step=24,
        ),
    },
    {
        "id": "design_indian",
        "tool": "design",
        "label": "indian accent",
        "tag": "design",
        "args": dict(
            text="Welcome, my friend. Today I will tell you about the wonders of the universe.",
            instruct="male, young adult, indian accent",
            language="English",
            num_step=24,
        ),
    },
    {"id": "lang_en", "tool": "tts", "label": "English", "tag": "lang",
     "args": dict(text="Hello, how are you today? It's a beautiful morning.",
                  language="English", num_step=20)},
    {"id": "lang_es", "tool": "tts", "label": "Spanish", "tag": "lang",
     "args": dict(text="Hola, ¿cómo estás hoy? Es una mañana hermosa.",
                  language="Spanish", num_step=20)},
    {"id": "lang_fr", "tool": "tts", "label": "French", "tag": "lang",
     "args": dict(text="Bonjour, comment allez-vous aujourd'hui ? C'est une belle matinée.",
                  language="French", num_step=20)},
    {"id": "lang_de", "tool": "tts", "label": "German", "tag": "lang",
     "args": dict(text="Hallo, wie geht es Ihnen heute? Es ist ein wunderschöner Morgen.",
                  language="German", num_step=20)},
    {"id": "lang_ja", "tool": "tts", "label": "Japanese", "tag": "lang",
     "args": dict(text="こんにちは、お元気ですか。今朝はとても素敵な朝です。",
                  language="Japanese", num_step=20)},
    {"id": "lang_zh", "tool": "tts", "label": "Chinese (Mandarin)", "tag": "lang",
     "args": dict(text="你好，今天过得怎么样？今早天气真好。",
                  language="Chinese", num_step=20)},
    {"id": "lang_ar", "tool": "tts", "label": "Arabic", "tag": "lang",
     "args": dict(text="مرحباً، كيف حالك اليوم؟ إنه صباح جميل.",
                  language="Arabic", num_step=20)},
    {"id": "tag_laughter", "tool": "tts", "label": "[laughter] tag", "tag": "tags",
     "args": dict(text="[laughter] You really got me with that one! I didn't see it coming.",
                  language="English", num_step=20)},
    {"id": "tag_sigh", "tool": "tts", "label": "[sigh] tag", "tag": "tags",
     "args": dict(text="[sigh] Another long day at the office.",
                  language="English", num_step=20)},
    {"id": "clone_demo", "tool": "clone", "label": "voice clone (ref = hello_auto)", "tag": "clone",
     "args": dict(
        text="This is the cloned voice speaking different words but in the same style.",
        ref_audio=str(OUT / "hello_auto.wav"),
        language="English",
        num_step=24,
    )},
]


def to_mp3(wav: Path):
    if not shutil.which("ffmpeg"):
        return None
    mp3 = wav.with_suffix(".mp3")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
             "-codec:a", "libmp3lame", "-qscale:a", "4", str(mp3)],
            check=True,
        )
        return mp3
    except Exception as e:
        print(f"  ⚠️  mp3 convert failed: {e}")
        return None


def main() -> int:
    print(f"📁 Output: {OUT}")
    print("🔥 Warming model...")
    omnivoice_load_model()
    manifest = []
    t_total = time.time()

    for s in SAMPLES:
        wav = OUT / f"{s['id']}.wav"
        s["args"]["output"] = str(wav)
        print(f"\n→ {s['id']:25s} ({s['tool']:6s}) — {s['label']}")
        t0 = time.time()
        if s["tool"] == "tts":
            r = omnivoice_tts(**s["args"])
        elif s["tool"] == "design":
            r = omnivoice_design(**s["args"])
        elif s["tool"] == "clone":
            r = omnivoice_clone(**s["args"])
        else:
            print("  ❌ unknown tool")
            continue
        dt = time.time() - t0
        if r["status"] != "success":
            print(f"  ❌ {r['content'][0]['text']}")
            continue
        d = r["content"][1]["json"]
        print(f"  ✅ {dt:.1f}s · {d['duration_s']:.2f}s audio")
        mp3 = to_mp3(wav)
        if mp3:
            print(f"  ➜ mp3 {mp3.stat().st_size / 1024:.1f} KB")

        manifest.append({
            "id": s["id"], "tool": s["tool"], "label": s["label"], "tag": s["tag"],
            "wav": f"assets/audio/{wav.name}",
            "mp3": f"assets/audio/{mp3.name}" if mp3 else None,
            "duration_s": d["duration_s"],
            "args": {k: v for k, v in s["args"].items() if k != "output"},
        })

    manifest_path = OUT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"\n📜 manifest → {manifest_path} ({len(manifest)} samples)")
    print(f"⏱  total: {time.time() - t_total:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
