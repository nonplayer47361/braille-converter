import pytest
from braille_converter.common.translator import text_to_braille, braille_to_text

@pytest.mark.parametrize("txt, expected", [
    ("HelloWorld", "HelloWorld"),
    ("Test, 123!", "Test,123!"),
])
def test_text_to_braille_roundtrip(txt, expected, braille_logger):
    braille_logger.info(f"INPUT      → {txt!r}")
    b = text_to_braille(txt, lang="eng")
    braille_logger.info(f"BRAILLE    → {b}")
    decoded = braille_to_text(b, lang="eng")
    braille_logger.info(f"DECODED    → {decoded!r}")
    assert decoded == expected
    braille_logger.info("RESULT     → PASS\n")