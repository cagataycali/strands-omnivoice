"""02: Voice cloning — clone the speaker in /tmp/ref.wav.

Provide your own reference clip first:
    say -v Samantha "This is a sample reference for voice cloning." -o /tmp/ref.wav --data-format=LEF32@24000
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from strands import Agent
from strands_omnivoice import (
    omnivoice_clone,
    omnivoice_transcribe,
    audio_probe,
    audio_play,
)

print("=== 02: Voice Cloning ===")
t0 = time.time()

if not os.path.exists("/tmp/ref.wav"):
    print("⚠️  /tmp/ref.wav not found.")
    print("   Create one (macOS): say -v Samantha 'This is a reference clip' -o /tmp/ref.wav --data-format=LEF32@24000")
    sys.exit(1)

agent = Agent(tools=[audio_probe, omnivoice_transcribe, omnivoice_clone, audio_play])
agent(
    """1. audio_probe /tmp/ref.wav.
2. omnivoice_transcribe it to confirm content.
3. omnivoice_clone with text='In a parallel universe, machines speak softly.'
   ref_audio=/tmp/ref.wav output=/tmp/strands_omnivoice_02.wav.
4. audio_play /tmp/strands_omnivoice_02.wav."""
)

print(f"\nTotal time: {time.time() - t0:.1f}s")
print("=== PASS ===")
