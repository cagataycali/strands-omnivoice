# API Reference

<p class="so-intro">Every public tool, signature, and parameter — at a glance.</p>

> All tools live in `strands_omnivoice` and are decorated with `@tool` from `strands`.

## Synthesis

### `omnivoice_tts(text, output, language="", duration=0.0, speed=1.0, num_step=32, guidance_scale=2.0, model_id="", device="")`

Auto-voice synthesis. The model picks a voice. Returns the WAV path and metadata.

### `omnivoice_clone(text, output, ref_audio, ref_text="", language="", duration=0.0, speed=1.0, num_step=32, guidance_scale=2.0, model_id="", device="")`

Clone a speaker from `ref_audio`. If `ref_text` is empty, OmniVoice auto-transcribes via Whisper.

### `omnivoice_design(text, output, instruct, language="", duration=0.0, speed=1.0, num_step=32, guidance_scale=2.0, model_id="", device="")`

Voice design. `instruct` is a comma-separated attribute string (`"female, british accent"`).

### `omnivoice_batch(items, output_dir, num_step=32, guidance_scale=2.0, model_id="", device="")`

Batch synthesis sharing a single loaded model. Each item: `{"id":..., "text":..., "ref_audio"?:..., "instruct"?:..., ...}`.

## ASR

### `omnivoice_transcribe(audio_path, model_id="", device="")`

Transcribe an audio file using OmniVoice's bundled Whisper ASR.

## Model Lifecycle

### `omnivoice_load_model(model_id="", device="", dtype="", force=False)`

Pre-load (or reload) the model. Use as a warmup tool.

### `omnivoice_unload_model()`

Drop the cached model and free GPU memory.

### `omnivoice_download_model(model_id="k2-fsa/OmniVoice")`

Snapshot-download the checkpoint from HuggingFace Hub without loading.

## Info

### `omnivoice_sysinfo()`

Reports device, dtype, omnivoice version, torch info, and currently-loaded model state.

### `omnivoice_list_languages(filter="")`

List the supported language names; optionally filter by substring.

## Audio Utilities

### `audio_probe(audio_path)`

Inspect an audio file (duration, sample rate, channels, format).

### `audio_play(audio_path, blocking=False)`

Play an audio file using the host's default player. Supports macOS (`afplay`), Linux (`aplay`/`paplay`/`ffplay`).

## Web UI

### `omnivoice_demo_serve(action="start", ip="0.0.0.0", port=8001, model_id="")`

Manage the upstream `omnivoice-demo` Gradio web UI as a background process. Actions: `start` / `stop` / `status` / `logs`.

## Loader API (advanced)

### `get_model(model_id=None, device=None, dtype=None, force=False)`

Return the cached `OmniVoice` instance. Loads on first call.

### `unload_model()`

Drop cached weights and free GPU.

### `get_loaded_info()`

Inspect the cache state.

### `best_device()`

Auto-detect the best available backend (`cuda` → `mps` → `cpu`).
