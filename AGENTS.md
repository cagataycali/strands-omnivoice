# strands-omnivoice — AGENTS.md

**Living dev contract for any agent (human, Claude, GPT, Gemini) working on strands-omnivoice.**

---

## The 30-Second Pitch

**strands-omnivoice = Multilingual zero-shot TTS toolkit for Strands Agents.**

- **Upstream**: [k2-fsa/OmniVoice](https://github.com/k2-fsa/OmniVoice) — diffusion-LM TTS, 600+ languages, RTF 0.025
- **13 Tools**: auto TTS, voice clone, voice design, batch, ASR transcribe, model lifecycle, info/sysinfo, audio probe/play, Gradio demo
- **Singleton loader**: shared model instance across tools (huge win — no double-load)
- **Auto-device**: cuda → mps → cpu, override via env vars
- **Pure tools**: no custom Model provider; use any LLM as agent brain

---

## Core Principles

1. **RUN FIRST** — `pip install strands-omnivoice` → `from strands_omnivoice import omnivoice_tts` works.
2. **TOOLS, NOT MODELS** — OmniVoice is a TTS, not a chat LLM. We expose it as `@tool` functions.
3. **UPSTREAM UNTOUCHED** — `omnivoice` is a regular pip dep; we never fork or vendor.
4. **ONE MODEL, MANY TOOLS** — every tool calls `_loader.get_model()`; tools share one instance.
5. **THIN WRAPPERS** — every tool ≤ ~120 lines; the heavy lifting is `OmniVoice.generate()`.

---

## Repo Layout

```
strands-omnivoice/
├── AGENTS.md                       # this file
├── README.md                       # install + quickstart + tool table
├── pyproject.toml                  # v0.1.0, Apache-2.0
├── strands-omnivoice-logo.svg      # animated logo (multi-language sparkles)
├── agent.py                        # smoke-test agent loading every tool
├── strands_omnivoice/              # the package
│   ├── __init__.py                 # exports 13 tools + loader API
│   ├── _common.py                  # ok()/err() ToolResult builders
│   ├── _loader.py                  # singleton OmniVoice loader
│   └── tools/
│       ├── __init__.py
│       ├── tts.py                  # omnivoice_tts (auto voice)
│       ├── clone.py                # omnivoice_clone
│       ├── design.py               # omnivoice_design
│       ├── batch.py                # omnivoice_batch
│       ├── transcribe.py           # omnivoice_transcribe (ASR)
│       ├── model_lifecycle.py      # load/unload/download
│       ├── info.py                 # sysinfo + list_languages
│       ├── audio_utils.py          # audio_probe + audio_play
│       └── demo_server.py          # omnivoice_demo_serve (Gradio bg)
├── examples/                       # 5 runnable examples
│   ├── 01_basic_tts.py
│   ├── 02_voice_clone.py
│   ├── 03_voice_design.py
│   ├── 04_batch_multilingual.py
│   └── 05_agent_workflow.py
├── tests/                          # pytest suite
│   ├── __init__.py
│   ├── test_imports.py
│   ├── test_tool_specs.py
│   └── test_info_tools.py          # sysinfo / list_languages — no model load
├── docs/                           # MkDocs Material site
│   ├── index.md
│   ├── api-reference.md
│   ├── architecture.md
│   ├── getting-started/
│   │   ├── installation.md
│   │   └── quickstart.md
│   ├── guide/
│   │   ├── voice-cloning.md
│   │   ├── voice-design.md
│   │   ├── batch.md
│   │   └── apple-silicon.md
│   └── examples/
│       └── overview.md
├── mkdocs.yml
├── .github/workflows/
│   ├── ci.yml                      # lint + import-test
│   └── docs.yml                    # mkdocs deploy
├── LICENSE                         # Apache 2.0
└── LICENSE.notice                  # upstream attribution
```

---

## Hardware Support

| Platform | Backend | Status |
|---|---|---|
| Apple Silicon (M-series) | MPS | ✅ default |
| NVIDIA CUDA 12+ | cuda | ✅ |
| CPU (any) | cpu | ✅ (slow) |
| Jetson AGX Thor / Orin | cuda | 🟡 expected to work, untested |

`omnivoice_sysinfo` tool reveals the live state.

---

## Dependencies Policy

**Core** (always): `strands-agents`, `omnivoice>=0.1.5`, `soundfile`, `numpy`

**Optional**:
- `[demo]` — `gradio` for the demo server tool
- `[dev]`  — `pytest`, `ruff`
- `[all]`  — everything

**No vendoring** — `omnivoice` is a hard pip dep, never copied into this repo.

---

## Tool Architecture

Every tool follows the same pattern:

```python
from strands import tool
from .._common import ok, err, resolve_path, ensure_parent
from .._loader import get_model

@tool
def omnivoice_<verb>(text: str, output: str, ...):
    """Docstring describing the tool, its modes, and parameters."""
    # 1) validate inputs
    # 2) resolve paths
    # 3) get_model() — singleton load
    # 4) call model.generate(...)
    # 5) write WAV via soundfile
    # 6) return ok(text=..., data=...) or err(...)
```

This means:
- **Same loader, no double-load** — `omnivoice_clone` then `omnivoice_design` reuse weights.
- **Cheap import** — `from strands_omnivoice import …` doesn't import torch/omnivoice; first tool call does.
- **Symmetric tool results** — every tool returns the same shape.

---

## Key Workflows

### 1. Quick agent

```python
from strands import Agent
from strands_omnivoice import omnivoice_tts, omnivoice_sysinfo, audio_play

agent = Agent(tools=[omnivoice_tts, omnivoice_sysinfo, audio_play])
agent("Show sysinfo, then synth 'Hello' to /tmp/h.wav and play it.")
```

### 2. Voice cloning pipeline

```python
agent("""
1. Use omnivoice_transcribe on /tmp/ref.wav to get the transcript.
2. Then omnivoice_clone with that transcript and target text 'Hello in target voice'
   to /tmp/cloned.wav.
3. audio_play it.
""")
```

### 3. Batch synthesis

```python
agent("""
omnivoice_batch with items=[
  {"id": "en", "text": "Hello",   "instruct": "female, british accent"},
  {"id": "fr", "text": "Bonjour", "instruct": "male, young adult"},
  {"id": "zh", "text": "你好",    "instruct": "女, 四川话"},
] output_dir=/tmp/batch
""")
```

---

## Development

```bash
git clone https://github.com/cagataycali/strands-omnivoice && cd strands-omnivoice
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

pytest -q                    # tests
ruff check strands_omnivoice # lint
ruff format strands_omnivoice
python agent.py              # smoke test (lists tools)
```

---

## Multi-Agent Coordination (Zenoh peers)

When multiple agents work on this repo concurrently:

1. `git fetch origin main` BEFORE editing.
2. Broadcast claim: `zenoh_peer(action='broadcast', message="[claim] tools/clone.py")`.
3. Wait 30s, silence → proceed.
4. Atomic commits: `[<agent-id>] <area>: <change>`.
5. **Append-only to AGENTS.md** — never rewrite another agent's log entries.

### Lane Ownership

| Lane | Owner | Scope |
|------|-------|-------|
| Loader | — | `_loader.py`, `_common.py` |
| Synth tools | — | `tts.py`, `clone.py`, `design.py`, `batch.py` |
| ASR tool | — | `transcribe.py` |
| Lifecycle | — | `model_lifecycle.py` |
| Info / utils | — | `info.py`, `audio_utils.py`, `demo_server.py` |
| Docs | — | `docs/`, `mkdocs.yml` |
| Examples | — | `examples/` |
| Tests | — | `tests/` |
| CI | — | `.github/workflows/`, `pyproject.toml` |

---

## Current Status

| Area | State | Notes |
|------|-------|-------|
| 13 Tools | ✅ shipped | Auto/clone/design/batch + ASR + lifecycle + utils + demo |
| Singleton loader | ✅ stable | Thread-safe, env-var configurable |
| Apple Silicon | ✅ verified | MPS default on macOS |
| CUDA | 🟡 untested in CI | Should JustWork™ — same upstream call paths |
| PyPI | 🔴 not yet | First release pending |
| Docs site | 🟢 scaffold ready | Needs content fill-in |
| CI | ✅ ci.yml + docs.yml | Lint + import test |
| Tests | 🟡 minimal | Imports + tool specs + info tools (no model-load) |

---

## What Needs Work

1. **Real generation tests** — currently CI only tests imports + sysinfo. Add a heavy nightly job that loads the model and generates a WAV.
2. **Streaming output** — OmniVoice supports chunked generation (`audio_chunk_duration`); expose it as a tool option.
3. **Voice library** — common reference clips bundled or hosted, addressable by name (`ref="emma_british"`).
4. **Speaker similarity eval** — built-in tool to score cloning quality (cosine on speaker embeddings).
5. **CUDA + Jetson verification** — confirm pipeline on a real Jetson Thor.

---

## Append-Only Context Learning Log

> New entries go AT THE TOP.

### 2026-05-16 — Initial scaffold

Built strands-omnivoice from scratch using strands-cosmos as a structural template.
Key decisions:
- **Tools-only design** (no `Model` provider) because OmniVoice is TTS, not a chat LLM.
- **Singleton loader** to share a single ~hundreds-of-MB checkpoint across tools.
- **Lazy imports** of torch/omnivoice inside tool bodies → cheap top-level import.
- 13 tools cover all 3 generation modes + ASR + lifecycle + info + audio utils + Gradio.
- Logo: animated SVG with multi-language symbols (A/中/ا/日/Ω/ñ) floating along a
  warm pink/orange "voice strand" alongside the green Strands ribbon, plus
  pulsing soundwave rings around a central microphone node.
- Verified on Apple Silicon MPS, omnivoice 0.1.5, torch 2.12.

---
