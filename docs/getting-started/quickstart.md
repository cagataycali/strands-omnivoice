# Quickstart

<p class="so-intro">A two-minute tour of every voice mode — auto, design, and clone.</p>

A minimal end-to-end example.

```python
from strands import Agent
from strands_omnivoice import (
    omnivoice_tts, omnivoice_clone, omnivoice_design,
    omnivoice_sysinfo, audio_play,
)

agent = Agent(tools=[
    omnivoice_tts, omnivoice_clone, omnivoice_design,
    omnivoice_sysinfo, audio_play,
])

# 1. Sanity check
agent("omnivoice_sysinfo")

# 2. Auto voice
agent("omnivoice_tts text='Hello world' output=/tmp/hello.wav, then audio_play it")
```

<div class="so-audio"
     data-src="../assets/audio/hello_auto.mp3"
     data-label="result · hello_auto.wav"
     data-tag="auto"
     data-text='"Hello world, welcome to Strands OmniVoice — multilingual zero-shot text to speech."'></div>

## Direct Tool Calls (No Agent)

Each `@tool` is just a function — call it directly:

```python
from strands_omnivoice import omnivoice_tts

result = omnivoice_tts(text="Hello", output="/tmp/h.wav")
print(result["content"][0]["text"])
# → "🔊 wrote /tmp/h.wav (1.23s @ 24000 Hz)"
```

## Three Generation Modes — All Real Samples

=== "Auto"

    ```python
    omnivoice_tts(
        text="Hello world.",
        output="/tmp/auto.wav",
        language="English",
    )
    ```

    <div class="so-audio"
         data-src="../assets/audio/lang_en.mp3"
         data-label="auto · english"
         data-tag="auto"
         data-text='"Hello, how are you today? It is a beautiful morning."'></div>

=== "Design"

    ```python
    omnivoice_design(
        text="Once upon a time, in a land far far away.",
        instruct="female, elderly, low pitch, british accent",
        output="/tmp/story.wav",
    )
    ```

    <div class="so-audio"
         data-src="../assets/audio/design_uk_elderly.mp3"
         data-label="british elderly female"
         data-tag="design"
         data-text='"Once upon a time, in a land far far away, there lived a wise old story-teller."'></div>

=== "Clone"

    ```python
    omnivoice_clone(
        text="This is the cloned voice speaking different words.",
        ref_audio="/tmp/hello.wav",
        output="/tmp/cloned.wav",
    )
    ```

    <div class="so-audio"
         data-src="../assets/audio/clone_demo.mp3"
         data-label="cloned voice"
         data-tag="clone"
         data-text='"This is the cloned voice speaking different words but in the same style."'></div>

## Model Pre-warming

To avoid load-latency on the first synthesis, pre-warm:

```python
from strands_omnivoice import omnivoice_load_model

omnivoice_load_model(device="mps")  # or "cuda", or leave empty for auto
```

Subsequent calls reuse the cached weights — zero double-load even when chaining
`omnivoice_clone` → `omnivoice_design` → `omnivoice_tts`.

## Running the Smoke-test Agent

```bash
python agent.py "Show sysinfo, then synth 'привет мир' to /tmp/ru.wav and play it"
```

The `agent.py` script in the repo loads all 13 tools and gives the LLM full
creative freedom.

→ [Voice Cloning Guide](../guide/voice-cloning.md) · [Voice Design Guide](../guide/voice-design.md)
