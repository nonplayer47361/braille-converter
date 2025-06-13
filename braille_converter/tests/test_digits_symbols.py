import pytest
from braille_converter.common.translator import text_to_braille_num_special
from braille_converter.english.english_translator import decode

@pytest.mark.parametrize("src, expected", [
    # 순수 숫자
    ("0123456789", "0123456789"),
    # 순수 특수문자
    (",.!?@#", ",.!?@#"),
    # 숫자+특수문자 조합
    ("Phone #42, ext. 101", "42#,101"),
])
def test_roundtrip_digits_and_symbols(src, expected, braille_logger):
    braille_logger.info(f"INPUT      → {src!r} (digits & symbols only)")
    braille = text_to_braille_num_special(src, lang="eng")
    braille_logger.info(f"BRAILLE    → {braille}")
    result = decode(braille)
    braille_logger.info(f"DECODED    → {result!r}")
    assert result == expected
    braille_logger.info("RESULT     → PASS\n")