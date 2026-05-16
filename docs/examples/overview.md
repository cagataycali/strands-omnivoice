# Examples

<p class="so-intro">Five runnable scripts demonstrating every voice mode end-to-end.</p>

The repo's `examples/` directory contains five runnable scripts:

| File | Demonstrates |
|---|---|
| [`01_basic_tts.py`](https://github.com/cagataycali/strands-omnivoice/blob/main/examples/01_basic_tts.py) | Auto-voice synthesis + sysinfo + audio playback |
| [`02_voice_clone.py`](https://github.com/cagataycali/strands-omnivoice/blob/main/examples/02_voice_clone.py) | Voice cloning from a reference WAV (with ASR step) |
| [`03_voice_design.py`](https://github.com/cagataycali/strands-omnivoice/blob/main/examples/03_voice_design.py) | Voice design — three different attribute combos |
| [`04_batch_multilingual.py`](https://github.com/cagataycali/strands-omnivoice/blob/main/examples/04_batch_multilingual.py) | Batch synthesis across 7 languages with mixed modes |
| [`05_agent_workflow.py`](https://github.com/cagataycali/strands-omnivoice/blob/main/examples/05_agent_workflow.py) | Full agent loaded with every tool, end-to-end |

## Running

```bash
git clone https://github.com/cagataycali/strands-omnivoice
cd strands-omnivoice
python -m venv .venv && source .venv/bin/activate
pip install -e .

# Need an LLM to drive the agent — e.g. Anthropic on Bedrock:
export AWS_BEARER_TOKEN_BEDROCK=...
python examples/01_basic_tts.py
```

The first run downloads the OmniVoice checkpoint (~1 GB).
