"""01: Basic auto-voice TTS — no reference, no instruct."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from strands import Agent
from strands_omnivoice import omnivoice_sysinfo, omnivoice_tts, audio_play

print("=== 01: Basic Auto-Voice TTS ===")
t0 = time.time()

agent = Agent(tools=[omnivoice_sysinfo, omnivoice_tts, audio_play])
agent(
    "First show sysinfo. Then synthesize 'Hello world, this is OmniVoice running on Strands.' "
    "to /tmp/strands_omnivoice_01.wav and play it."
)

print(f"\nTotal time: {time.time() - t0:.1f}s")
print("=== PASS ===")
