from saysynth.lib import say


def test_gen_data_format_arg():
    data_format = say._gen_data_format_arg("AIFF", "LE", "F", 32, 22050)
    assert data_format == "BEF32@22050"
    data_format = say._gen_data_format_arg("WAVE", "LE", "F", 32, 22050)
    assert data_format == "LEF32@22050"
    data_format = say._gen_data_format_arg("WAVE", "LE", "F", 16, 22050)
    assert data_format == "LEF32@22050"
