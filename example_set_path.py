import os
import louis

# 1) Homebrew liblouis 테이블 디렉터리 경로
BREW_PREFIX = os.popen("brew --prefix", "r").read().strip()
TABLE_DIR   = os.path.join(BREW_PREFIX, "share/liblouis/tables")

# 2) 원본 translateString 저장
_orig_translate = louis.translateString

# 3) translateString 래퍼 정의
def translateString(tables, text, **kwargs):
    """tables 리스트에 bare-name을 넘기면 .ctb를 붙이고
       full-path로 자동 변환해 줍니다."""
    paths = []
    for t in tables:
        # 이미 절대경로이면 그대로, 아니면 TABLE_DIR + name.ctb
        if os.path.isabs(t):
            paths.append(t)
        else:
            name = t
            # 확장자 생략 시 .ctb 추가
            if not name.lower().endswith(".ctb"):
                name = name + ".ctb"
            paths.append(os.path.join(TABLE_DIR, name))
    return _orig_translate(paths, text, **kwargs)

# 4) monkey-patch
louis.translateString = translateString

# 5) 테스트
if __name__ == "__main__":
    result = louis.translateString(["en-us-g2"], "Hello")
    print(result)   # ⠓⠑⠇⠇⠕