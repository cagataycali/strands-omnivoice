"""Regression test: omnivoice_transcribe must accept the documented args."""

from strands_omnivoice import omnivoice_transcribe


def test_transcribe_signature_includes_asr_model_name():
    """The ASR model is loaded lazily — exposing this kwarg lets callers override."""
    spec = omnivoice_transcribe.tool_spec
    props = spec["inputSchema"]["json"]["properties"]
    assert "audio_path" in props
    assert "asr_model_name" in props


def test_transcribe_returns_error_on_missing_file():
    r = omnivoice_transcribe(audio_path="/tmp/__definitely_not_a_file__.wav")
    assert r["status"] == "error"
