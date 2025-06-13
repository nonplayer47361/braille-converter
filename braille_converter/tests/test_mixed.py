import pytest

from braille_converter.english.english_translator import encode, decode
from braille_converter.common.translator import (
    text_to_braille_alpha,
    text_to_braille_num_special,
)

@pytest.mark.parametrize(
    "text, form, expected",
    [
        # mixed-language roundtrip in both unicode and dots forms
        ("HelloWorld", 'unicode', "HelloWorld"),
        ("HelloWorld", 'dots',    "HelloWorld"),
        ("HELLOWORLD", 'unicode', "HELLOWORLD"),
        ("helloworld", 'unicode', "helloworld"),
        ("Test, 123!", 'unicode', "Test,123!"),
        ("Test, 123!", 'dots',    "Test,123!"),
        ("Hello, World! 123", 'unicode', "Hello,World!123"),
        ("Hello, World! 123", 'dots',    "Hello,World!123"),
    ]
)
def test_roundtrip_mixed_unicode_and_dots(text, form, expected, braille_logger):
    braille_logger.info(f"INPUT      → {text!r} (form={form})")
    b = encode(text, form=form)
    braille_logger.info(f"BRAILLE    → {b}")
    result = decode(b)
    braille_logger.info(f"DECODED    → {result!r}")
    assert result == expected
    braille_logger.info("RESULT     → PASS\n")

def test_letters_only_mode(src="Hello, World! 123", braille_logger=None):
    src = "Hello, World! 123"
    braille_logger.info(f"INPUT      → {src!r} (letters_only)")
    b = text_to_braille_alpha(src, lang="eng")
    braille_logger.info(f"BRAILLE    → {b}")
    result = decode(b)
    braille_logger.info(f"DECODED    → {result!r}")
    assert result == "HelloWorld"
    braille_logger.info("RESULT     → PASS\n")

def test_numbers_and_special_only_mode(src="Hello, World! 123", braille_logger=None):
    src = "Hello, World! 123"
    braille_logger.info(f"INPUT      → {src!r} (numbers_and_special_only)")
    b = text_to_braille_num_special(src, lang="eng")
    braille_logger.info(f"BRAILLE    → {b}")
    result = decode(b)
    braille_logger.info(f"DECODED    → {result!r}")
    assert result == ",!123"
    braille_logger.info("RESULT     → PASS\n")