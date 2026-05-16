"""04: Batch synthesis across multiple languages with mixed voice modes."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from strands import Agent
from strands_omnivoice import omnivoice_batch

print("=== 04: Batch Multilingual ===")
t0 = time.time()

ITEMS = [
    {"id": "en_uk",   "text": "Good evening, the weather is splendid.",
     "instruct": "female, british accent"},
    {"id": "en_us",   "text": "Hey, how's it going? Long time no see.",
     "instruct": "male, american accent"},
    {"id": "es",      "text": "Hola, ¿cómo estás hoy?",
     "instruct": "female, young adult", "language": "Spanish"},
    {"id": "fr",      "text": "Bonjour, comment allez-vous ?",
     "instruct": "male, middle-aged", "language": "French"},
    {"id": "de",      "text": "Guten Tag, wie geht es Ihnen?",
     "instruct": "female, elderly", "language": "German"},
    {"id": "ja",      "text": "こんにちは、お元気ですか。",
     "language": "Japanese"},
    {"id": "zh_sich", "text": "你今天吃了没得？",
     "instruct": "男, 青年, 四川话", "language": "Chinese"},
]

agent = Agent(tools=[omnivoice_batch])
agent(
    f"omnivoice_batch with output_dir=/tmp/strands_omnivoice_batch and items={ITEMS}"
)

print(f"\nTotal time: {time.time() - t0:.1f}s")
print("=== PASS ===")
