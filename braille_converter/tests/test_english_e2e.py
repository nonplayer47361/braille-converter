import pytest
from braille_converter.english.english_translator import encode, decode

@pytest.mark.parametrize("text, expected", [
    # 1. 모두 소문자
    ("helloworld", "helloworld"),
    # 2. 모두 대문자
    ("HELLOWORLD", "HELLOWORLD"),
    # 3. 혼합 대/소문자
    ("HelloWorld",  "HelloWorld"),
])
def test_roundtrip_english_only(text, expected, braille_logger):
    braille_logger.info(f"INPUT      → {text!r} (english only)")
    # 점자 변환은 unicode 형식으로 고정
    braille = encode(text, form="unicode")
    braille_logger.info(f"BRAILLE    → {braille}")
    result = decode(braille)
    braille_logger.info(f"DECODED    → {result!r}")
    assert result == expected
    braille_logger.info("RESULT     → PASS\n")