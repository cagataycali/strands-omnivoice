# Installation

<p class="so-intro">Install in 60 seconds. Pick the PyTorch flavour that matches your hardware and you're done.</p>

## TL;DR

```bash
pip install strands-omnivoice
```

This pulls in `omnivoice>=0.1.5`, `strands-agents`, `soundfile`, and `numpy`. It does **not** force a particular PyTorch flavour — pick yours below.

## PyTorch by Hardware

=== "NVIDIA (CUDA)"

    ```bash
    pip install torch==2.8.0+cu128 torchaudio==2.8.0+cu128 \
        --extra-index-url https://download.pytorch.org/whl/cu128
    ```

=== "Apple Silicon (MPS)"

    ```bash
    pip install torch==2.8.0 torchaudio==2.8.0
    ```

=== "CPU only"

    ```bash
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
    ```

    Generation is slow on CPU. Use only for development or low-volume jobs.

## Verifying

```bash
python -c "
from strands_omnivoice import omnivoice_sysinfo
import json
print(json.dumps(omnivoice_sysinfo(), indent=2, default=str))
"
```

You should see your detected device, torch version, and `omnivoice_version`.

## Optional Extras

```bash
pip install 'strands-omnivoice[demo]'   # gradio (omnivoice_demo_serve)
pip install 'strands-omnivoice[dev]'    # pytest, ruff
pip install 'strands-omnivoice[all]'    # everything
```

## Troubleshooting

### `ImportError: cannot import name 'OmniVoice'`

`omnivoice` failed to install. Check the upstream's [installation guide](https://github.com/k2-fsa/OmniVoice#installation) for your platform.

### `RuntimeError: MPS device not available`

You're on macOS without Apple Silicon, or Python wasn't built for arm64. Pin device explicitly:

```bash
export STRANDS_OMNIVOICE_DEVICE=cpu
```

### Out of memory on first generation

OmniVoice loads ~1 GB of weights. Free GPU memory before calling `omnivoice_load_model`, or pass `device="cpu"`.
