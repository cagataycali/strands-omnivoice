"""05: Full agent workflow — load every tool, let the model orchestrate."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from strands import Agent
from strands_omnivoice import (
    audio_play,
    audio_probe,
    omnivoice_batch,
    omnivoice_clone,
    omnivoice_design,
    omnivoice_list_languages,
    omnivoice_load_model,
    omnivoice_sysinfo,
    omnivoice_transcribe,
    omnivoice_tts,
    omnivoice_unload_model,
)

print("=== 05: Full Agent Workflow ===")
t0 = time.time()

TOOLS = [
    omnivoice_sysinfo,
    omnivoice_load_model,
    omnivoice_list_languages,
    omnivoice_tts,
    omnivoice_clone,
    omnivoice_design,
    omnivoice_batch,
    omnivoice_transcribe,
    audio_probe,
    audio_play,
    omnivoice_unload_model,
]

agent = Agent(
    tools=TOOLS,
    system_prompt=(
        "You are a hands-on TTS assistant. Use omnivoice tools to satisfy the user "
        "request, parallelizing calls where possible. Always show sysinfo first."
    ),
)
agent(
    """Demo run:
    1. omnivoice_sysinfo
    2. omnivoice_load_model (warmup)
    3. omnivoice_list_languages filter='english'
    4. omnivoice_tts text='Welcome to strands-omnivoice.' output=/tmp/welcome.wav
    5. omnivoice_design text='I am a story-teller.' instruct='female, elderly, british accent'
       output=/tmp/storyteller.wav
    6. audio_play /tmp/storyteller.wav
    7. omnivoice_unload_model"""
)

print(f"\nTotal time: {time.time() - t0:.1f}s")
print("=== PASS ===")
