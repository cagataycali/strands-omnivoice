# Apple Silicon

<p class="so-intro">Run OmniVoice natively on M-series Macs via PyTorch's MPS backend.</p>

OmniVoice runs natively on Apple Silicon via PyTorch's MPS backend.

## Install

```bash
pip install strands-omnivoice
pip install torch==2.8.0 torchaudio==2.8.0
```

## Verify

```python
from strands_omnivoice import omnivoice_sysinfo
print(omnivoice_sysinfo())
```

You should see `device=mps`. The first call to any synthesis tool warms the model.

## Force a Device

```bash
export STRANDS_OMNIVOICE_DEVICE=mps   # or cpu, cuda
export STRANDS_OMNIVOICE_DTYPE=float16
```

Or per-call:

```python
omnivoice_tts(text="...", output="...", device="mps")
```

## Performance Tips

- **First call is slow** — checkpoint download + JIT warmup.
- Pre-warm with `omnivoice_load_model()` before user-facing latency matters.
- Lower `num_step` (16) trades a little quality for ~2x speed.
- Voice cloning with a 3-second reference is faster than 10s.

## Known Issues

- The first model load on a fresh machine downloads ~1 GB. Subsequent runs reuse the HuggingFace cache (`~/.cache/huggingface/hub/`).
- `whisper` ASR (used by `omnivoice_transcribe` and auto-transcription) currently runs on CPU even when synthesis is on MPS — a small one-time cost.
