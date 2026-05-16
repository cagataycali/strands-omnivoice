"""Test agent loading every strands-omnivoice tool.

Run after `pip install -e .` :

    python agent.py "Synthesize 'Hello world' to /tmp/hello.wav and play it."

Without args it just prints the registered tool roster.
"""
from __future__ import annotations

import sys

from strands import Agent

from strands_omnivoice import (
    audio_play,
    audio_probe,
    omnivoice_batch,
    omnivoice_clone,
    omnivoice_demo_serve,
    omnivoice_design,
    omnivoice_download_model,
    omnivoice_list_languages,
    omnivoice_load_model,
    omnivoice_sysinfo,
    omnivoice_transcribe,
    omnivoice_tts,
    omnivoice_unload_model,
)

TOOLS = [
    # synthesis
    omnivoice_tts,
    omnivoice_clone,
    omnivoice_design,
    omnivoice_batch,
    # ASR
    omnivoice_transcribe,
    # model lifecycle
    omnivoice_load_model,
    omnivoice_unload_model,
    omnivoice_download_model,
    # info
    omnivoice_sysinfo,
    omnivoice_list_languages,
    # audio utilities
    audio_probe,
    audio_play,
    # web UI
    omnivoice_demo_serve,
]


SYSTEM_PROMPT = """You are a multilingual TTS assistant powered by OmniVoice.

You have tools for:
- omnivoice_tts: simple auto-voice synthesis (text → wav)
- omnivoice_clone: voice cloning from a reference clip (3-10s)
- omnivoice_design: voice design via attributes (gender, age, accent, dialect, ...)
- omnivoice_batch: batch synthesis for multiple items at once
- omnivoice_transcribe: ASR via the bundled Whisper model
- omnivoice_load_model / omnivoice_unload_model / omnivoice_download_model: model lifecycle
- omnivoice_sysinfo / omnivoice_list_languages: introspection
- audio_probe / audio_play: inspect/play WAV files
- omnivoice_demo_serve: launch the upstream Gradio web UI in the background

Always:
- Run omnivoice_sysinfo first if you're unsure whether the host is GPU-ready.
- For voice cloning, prefer 3-10s reference audio in the same language.
- Use omnivoice_design with comma-separated attributes (e.g. "female, british accent").
- Output paths must be absolute or in /tmp.
"""


def main() -> int:
    print(f"🎤 strands-omnivoice agent · {len(TOOLS)} tools loaded:")
    for t in TOOLS:
        print(f"   · {t.tool_name}")
    print()

    if len(sys.argv) <= 1:
        print('Usage: python agent.py "your request"')
        print('Example: python agent.py "Show sysinfo, then say hello in English to /tmp/hello.wav"')
        return 0

    query = " ".join(sys.argv[1:])
    agent = Agent(tools=TOOLS, system_prompt=SYSTEM_PROMPT)
    agent(query)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
