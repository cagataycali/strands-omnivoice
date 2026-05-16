"""Make sure every public export imports cleanly without loading the model."""


def test_top_level_import():
    import strands_omnivoice as so

    assert so.__version__
    expected = {
        "omnivoice_tts",
        "omnivoice_clone",
        "omnivoice_design",
        "omnivoice_batch",
        "omnivoice_transcribe",
        "omnivoice_load_model",
        "omnivoice_unload_model",
        "omnivoice_download_model",
        "omnivoice_sysinfo",
        "omnivoice_list_languages",
        "audio_probe",
        "audio_play",
        "omnivoice_demo_serve",
    }
    missing = expected - set(so.__all__)
    assert not missing, f"missing exports: {missing}"


def test_loader_api_exposed():
    from strands_omnivoice import best_device, get_loaded_info, get_model, unload_model

    assert callable(best_device)
    assert callable(get_loaded_info)
    assert callable(get_model)
    assert callable(unload_model)
