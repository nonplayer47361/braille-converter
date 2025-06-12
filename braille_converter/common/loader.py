import unittest
from braille_converter.common.translator import text_to_braille, braille_to_text

class TestEnglishE2E(unittest.TestCase):
    def test_roundtrip_letters(self):
        txt = "HelloWorld"
        b = text_to_braille(txt, lang="eng")
        self.assertEqual(braille_to_text(b, lang="eng"), txt)

    def test_numbers_and_punct(self):
        txt = "Test, 123!"
        b = text_to_braille(txt, lang="eng")
        # spaces skipped, number indicator + patterns for digits, punctuation preserved
        decoded = braille_to_text(b, lang="eng")
        self.assertEqual(decoded, "Test,123!")

if __name__ == "__main__":
    unittest.main()