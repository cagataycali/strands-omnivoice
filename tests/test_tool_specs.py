"""Each tool must be a Strands @tool with a schema."""

import pytest

from strands_omnivoice import (
    audio_play,
    audio_probe,
    omnivoice_batch,
    omnivoice_clone,
    omnivoice_demo_serve,
    omnivoice_design,
    omnivoice_download_model,
    omnivoice_list_languages,
    omnivoice_load_model,
    omnivoice_sysinfo,
    omnivoice_transcribe,
    omnivoice_tts,
    omnivoice_unload_model,
)

ALL_TOOLS = [
    omnivoice_tts,
    omnivoice_clone,
    omnivoice_design,
    omnivoice_batch,
    omnivoice_transcribe,
    omnivoice_load_model,
    omnivoice_unload_model,
    omnivoice_download_model,
    omnivoice_sysinfo,
    omnivoice_list_languages,
    audio_probe,
    audio_play,
    omnivoice_demo_serve,
]


@pytest.mark.parametrize("tool", ALL_TOOLS, ids=lambda t: t.tool_name)
def test_tool_has_name_and_spec(tool):
    assert tool.tool_name, "tool has empty name"
    spec = tool.tool_spec
    assert spec["name"] == tool.tool_name
    assert spec.get("description"), f"{tool.tool_name} missing description"
    assert "inputSchema" in spec, f"{tool.tool_name} missing inputSchema"


def test_tool_names_unique():
    names = [t.tool_name for t in ALL_TOOLS]
    assert len(names) == len(set(names)), f"duplicates: {names}"


def test_tool_count():
    assert len(ALL_TOOLS) == 13
