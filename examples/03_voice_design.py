"""03: Voice design — describe the speaker via attributes."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from strands import Agent
from strands_omnivoice import omnivoice_design, audio_play

print("=== 03: Voice Design ===")
t0 = time.time()

agent = Agent(tools=[omnivoice_design, audio_play])
agent(
    """Use omnivoice_design THREE TIMES with these instructions:
    1. text='Once upon a time, in a land far away.' instruct='female, elderly, low pitch, british accent'
       output=/tmp/strands_omnivoice_03_a.wav
    2. text='Houston, we have a problem.' instruct='male, middle-aged, american accent'
       output=/tmp/strands_omnivoice_03_b.wav
    3. text='And then everything went silent.' instruct='female, young adult, whisper'
       output=/tmp/strands_omnivoice_03_c.wav
    Then audio_play each WAV in order."""
)

print(f"\nTotal time: {time.time() - t0:.1f}s")
print("=== PASS ===")
