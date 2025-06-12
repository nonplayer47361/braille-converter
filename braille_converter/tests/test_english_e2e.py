import unittest
import traceback
from pathlib import Path
from braille_converter.common.translator import (
    text_to_braille,
    text_to_braille_alpha,
    text_to_braille_num_special,
    braille_to_text,
)

#─── 절대 경로로 logs 디렉터리/파일 설정 ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent      # .../braille_converter
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "test_eng_e2e.log"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def _append(msg: str) -> None:
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg)

def _log(mode: str, input_text: str, braille: str, decoded: str) -> None:
    _append(f"[{mode}]\n")
    _append(f"input   : {input_text!r}\n")
    _append(f"braille : {braille}\n")
    _append(f"decoded : {decoded!r}\n")
    _append("-" * 40 + "\n")

def _log_error(mode: str, input_text: str, err: Exception) -> None:
    _append(f"[{mode} ERROR]\n")
    _append(f"input   : {input_text!r}\n")
    _append(f"error   : {err!r}\n")
    _append("traceback:\n")
    _append(traceback.format_exc())
    _append("-" * 40 + "\n")


class TestEnglishE2E(unittest.TestCase):
    def _run_case(self, mode, func, txt, expected=None):
        """
        func: 함수 호출 콜백(입력 문자열 → 변환된 텍스트 반환)
        """
        try:
            result = func(txt)
        except Exception as e:
            _log_error(mode, txt, e)
            raise
        else:
            # result 이 튜플일 때 (braille, decoded) 분리
            if isinstance(result, tuple):
                b, decoded = result
            else:
                # text_to_braille 계열만 braille 반환 → 디코딩 후 비교
                if mode.endswith("_mode"):
                    b = result
                    decoded = braille_to_text(b, lang="eng")
                else:
                    # roundtrip_letters, numbers_and_punct 등
                    b = result
                    decoded = braille_to_text(b, lang="eng")
            _log(mode, txt, b, decoded)
            if expected is not None:
                try:
                    self.assertEqual(decoded, expected)
                except AssertionError as ae:
                    _log_error(mode, txt, ae)
                    raise

    def test_roundtrip_letters(self):
        self._run_case(
            mode="roundtrip_letters",
            func=lambda s: text_to_braille(s, lang="eng"),
            txt="HelloWorld",
            expected="HelloWorld"
        )

    def test_numbers_and_punct(self):
        self._run_case(
            mode="numbers_and_punct",
            func=lambda s: text_to_braille(s, lang="eng"),
            txt="Test, 123!",
            expected="Test,123!"
        )

    def test_letters_only_mode(self):
        self._run_case(
            mode="letters_only_mode",
            func=lambda s: text_to_braille_alpha(s, lang="eng"),
            txt="Hello, World! 123",
            expected="HelloWorld"
        )

    def test_numbers_and_special_only_mode(self):
        self._run_case(
            mode="numbers_and_special_only_mode",
            func=lambda s: text_to_braille_num_special(s, lang="eng"),
            txt="Hello, World! 123",
            expected=",!123"
        )

    def test_mixed_roundtrip(self):
        self._run_case(
            mode="mixed_roundtrip",
            func=lambda s: text_to_braille(s, lang="eng"),
            txt="Hello, World! 123",
            expected="Hello,World!123"
        )


if __name__ == "__main__":
    unittest.main()