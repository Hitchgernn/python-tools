from python_tools.media.web_images.extractor import _split_srcset


def test_split_srcset():
    value = "a.jpg 1x, b.jpg 2x, c.jpg 3x"
    assert _split_srcset(value) == ["a.jpg", "b.jpg", "c.jpg"]
