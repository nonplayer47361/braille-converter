import subprocess
import os

# 1) LOUISTABLEPATH 가 설정되지 않았다면 여기서 세팅
BREW_PREFIX = os.popen("brew --prefix", "r").read().strip()
os.environ["LOUISTABLEPATH"] = f"{BREW_PREFIX}/share/liblouis/tables"

def translate_braille_g2(text: str) -> str:
    """
    lou_translate CLI를 호출해
    유니코드 브라유(⠓⠑⠇⠇⠕)를 리턴합니다.
    """
    # 테이블 확장자(.ctb)까지 명시
    tbl_arg = "unicode.dis,en-us-g2.ctb"
    args = ["lou_translate", "--forward", tbl_arg]

    proc = subprocess.run(
        args,
        input=text,
        text=True,            # UTF-8 디코딩
        capture_output=True,
        check=True
    )
    return proc.stdout.rstrip("\n")

if __name__ == "__main__":
    print( translate_braille_g2("Hello".capitalize()) )
    # 기대 출력: ⠠⠓⠑⠇⠇⠕