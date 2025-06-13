import pytest
from braille_converter.english.english_translator import encode, decode

@pytest.mark.parametrize("ch,expected", [
    ('a', '⠁'), ('z', '⠵'),
    ('A', '⠠⠁'), ('Z', '⠠⠵'),
])
def test_single_letters_unicode(ch, expected):
    assert encode(ch, form='unicode') == expected
    assert decode(expected) == ch.lower() if ch.islower() else ch