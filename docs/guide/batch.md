# Batch Synthesis

<p class="so-intro">Generate many WAVs in a single call, sharing one loaded model.</p>

Generate many WAVs in one call, sharing a single loaded model.

```python
from strands_omnivoice import omnivoice_batch

items = [
    {"id": "en", "text": "Hello world", "instruct": "female, british accent"},
    {"id": "fr", "text": "Bonjour le monde", "language": "French"},
    {"id": "ja", "text": "こんにちは", "language": "Japanese"},
]

omnivoice_batch(items=items, output_dir="/tmp/batch")
```

Output: `/tmp/batch/en.wav`, `/tmp/batch/fr.wav`, `/tmp/batch/ja.wav`.

## Item Schema

| Key | Required | Notes |
|---|---|---|
| `id` | ✅ | Output filename stem (`<id>.wav`) |
| `text` | ✅ | Text to synthesize |
| `ref_audio` | ❌ | Triggers **clone** mode |
| `ref_text` | ❌ | Optional reference transcript |
| `instruct` | ❌ | Triggers **design** mode |
| `language` | ❌ | Language hint (`English`, `en`, ...) |
| `duration` | ❌ | Fixed length in seconds |
| `speed` | ❌ | Speech speed factor |

If neither `ref_audio` nor `instruct` is set, the item runs in **auto** mode.

## JSON String / JSONL Path

For convenience, `items` can be:

- a Python list (above)
- a JSON-encoded string of a list
- a path to a `.jsonl` file (one item per line)

```python
omnivoice_batch(items="/path/to/test.jsonl", output_dir="/tmp/out")
```

## Multi-GPU Scaling

For thousands of items across multiple GPUs, use the upstream CLI directly:

```bash
omnivoice-infer-batch --model k2-fsa/OmniVoice --test_list test.jsonl --res_dir results/
```

`omnivoice_batch` is sequential — best for small/medium jobs.
