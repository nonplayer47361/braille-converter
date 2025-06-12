import unittest
from braille_converter.common.translator import text_to_braille, braille_to_text

class TestKoreanE2E(unittest.TestCase):
    def test_roundtrip_syllables(self):
        txt = "가나다라"
        b = text_to_braille(txt, lang="kor")
        self.assertEqual(braille_to_text(b, lang="kor"), txt)

    def test_mixed_syllables_and_punct(self):
        txt = "안녕, 세상!"
        b = text_to_braille(txt, lang="kor")
        decoded = braille_to_text(b, lang="kor")
        # 공백은 매핑되지 않으므로 제거하고 비교
        self.assertEqual(decoded.replace(" ", ""), "안녕,세상!")

if __name__ == "__main__":
    unittest.main()