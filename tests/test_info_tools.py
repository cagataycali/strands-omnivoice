"""Run the lightweight info tools — these don't load the heavy model."""

from strands_omnivoice.tools.info import omnivoice_list_languages, omnivoice_sysinfo


def test_sysinfo_runs():
    r = omnivoice_sysinfo()
    assert r["status"] == "success"
    text = r["content"][0]["text"]
    assert "OmniVoice" in text or "device" in text.lower()


def test_list_languages_returns_list():
    r = omnivoice_list_languages()
    assert r["status"] == "success"
    data = r["content"][1]["json"]
    assert data["count"] > 100  # OmniVoice supports 600+
    assert isinstance(data["languages"], list)


def test_list_languages_filter():
    r = omnivoice_list_languages(filter="english")
    assert r["status"] == "success"
    data = r["content"][1]["json"]
    assert all("english" in n.lower() for n in data["languages"])


def test_loader_info_when_unloaded():
    from strands_omnivoice import get_loaded_info, unload_model

    unload_model()
    info = get_loaded_info()
    assert info["loaded"] is False
    assert info["model_id"] is None
