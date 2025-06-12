import subprocess
import os
import re
from typing import List

# 1) LOUISTABLEPATH 설정 (없으면 여기서 세팅)
BREW_PREFIX = os.popen("brew --prefix", "r").read().strip()
os.environ["LOUISTABLEPATH"] = f"{BREW_PREFIX}/share/liblouis/tables"


def _lou_translate(text: str, tables: List[str]) -> str:
    """
    lou_translate CLI를 호출해 U+2800–U+28FF 브라유 점자 문자열을 리턴.
    tables 예: ["unicode.dis", "en-us-g1.ctb"]
    """
    arg = ",".join(tables)
    args = ["lou_translate", "--forward", arg]

    proc = subprocess.run(
        args,
        input=text,
        text=True,          # stdout를 UTF-8로 디코딩
        capture_output=True,
        check=True
    )
    return proc.stdout.rstrip("\n")


def translate_alpha(text: str) -> str:
    """
    영문자(A–Z, a–z)와 공백만 추출해 점자로 번역.
    """
    filtered = re.sub(r"[^A-Za-z\s]", "", text)
    return _lou_translate(filtered, ["unicode.dis", "en-us-g1.ctb"])


def translate_num_special(text: str) -> str:
    """
    숫자(0–9)와 특수문자만 추출해 점자로 번역.
    """
    filtered = re.sub(r"[A-Za-z\s]", "", text)
    return _lou_translate(filtered, ["unicode.dis", "en-us-g1.ctb"])


def translate_mixed(text: str) -> str:
    """
    원문 전체(영문+숫자+특수문자) 점자 번역.
    """
    return _lou_translate(text, ["unicode.dis", "en-us-g1.ctb"])


if __name__ == "__main__":
    s = "Hello, World! 123"
    print("영문만     :", translate_alpha(s))        # ⠓⠑⠇⠇⠕⠀⠺⠕⠗⠇⠙
    print("숫자·특수만 :", translate_num_special(s))  # ⠂⠠⠖⠒⠒⠒
    print("혼합      :", translate_mixed(s))         # ⠠⠓⠑⠇⠇⠕⠂⠀⠠⠺⠕⠗⠇⠙⠖⠁⠃⠉