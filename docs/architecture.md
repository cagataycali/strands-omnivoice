# Architecture

<p class="so-intro">How the singleton loader, lazy imports, and tools-only design fit together.</p>

```
┌──────────────────────────────────────────────────────────┐
│                  strands.Agent (your LLM)                │
└──────────────────────────────────────────────────────────┘
              │ calls @tool functions in parallel
              ▼
┌──────────────────────────────────────────────────────────┐
│  strands_omnivoice.tools/  (13 thin wrappers)            │
│  ├─ tts.py              ├─ batch.py                       │
│  ├─ clone.py            ├─ transcribe.py                 │
│  ├─ design.py           ├─ model_lifecycle.py            │
│  ├─ info.py             ├─ audio_utils.py                │
│  └─ demo_server.py                                        │
└──────────────────────────────────────────────────────────┘
              │ all tools call get_model()
              ▼
┌──────────────────────────────────────────────────────────┐
│       strands_omnivoice._loader (singleton)              │
│  ├─ Threading lock                                        │
│  ├─ (model_id, device) cache key                          │
│  └─ Lazy import of `omnivoice` + torch                   │
└──────────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────┐
│   omnivoice.OmniVoice  (k2-fsa upstream — pip install)   │
│  ├─ Diffusion-LM TTS architecture                        │
│  ├─ 600+ languages                                        │
│  ├─ Whisper ASR built-in                                  │
│  └─ HF Transformers backbone                              │
└──────────────────────────────────────────────────────────┘
```

## Why Tools, Not a Model Provider?

Strands `Model` providers are designed for **chat LLMs** that produce token streams.

OmniVoice is a **TTS model** that produces audio waveforms. Wrapping it as a `Model` would force an awkward chat-message API. Instead, we expose the three generation modes (`tts`/`clone`/`design`) plus utilities as `@tool` functions, and you bring your own LLM as the agent's brain.

## Singleton Loader Rationale

OmniVoice's checkpoint is a few hundred MB; a cold load can take 5-10 seconds plus the first-time HF download. If `omnivoice_clone` and `omnivoice_design` each loaded their own copy, agent workflows would be miserable.

`_loader.get_model()` caches by `(model_id, device)`. Multiple tools share the same instance; concurrent calls are serialized by a `threading.Lock`. To swap models, pass `force=True` or call `unload_model()` first.

## Lazy Imports

Top-level imports of `torch` and `omnivoice` are heavy. Tool bodies import them only when a tool is *called*. This means:

- `from strands_omnivoice import omnivoice_tts` is fast.
- `Agent(tools=[omnivoice_tts])` doesn't trigger any heavy import.
- The first `omnivoice_tts(...)` call is what loads the model.

## Tool Result Shape

Every tool returns the standard Strands tool-result dict:

```python
{
    "status": "success" | "error",
    "content": [
        {"text": "human-readable summary"},
        {"json": {"output": "/tmp/h.wav", ...}},
    ],
}
```

This makes the tools agent-, MCP-, and human-friendly.
