import sys
from pathlib import Path
from functools import lru_cache
from louis import Translator

# 언어별로 사용할 CTB 파일 경로를 지정
TABLE_FILES = {
    "eng": Path(__file__).parent.parent
                   / "liblouis_translator"
                   / "english"
                   / "en-us-g2.ctb",
    "kor": Path(__file__).parent.parent
                   / "liblouis_translator"
                   / "korean"
                   / "ko-g2.ctb",
}

@lru_cache()
def load_table(lang: str) -> dict:
    """
    liblouis CTB 테이블을 직접 읽어서
    글자 → 점자 패턴 매핑(dict)을 반환합니다.
    """
    if lang not in TABLE_FILES:
        raise ValueError(f"Unsupported language: {lang}")
    table_file = TABLE_FILES[lang]
    if not table_file.exists():
        raise FileNotFoundError(f"Braille table not found: {table_file}")

    # Translator: liblouis 바인딩 (pip install louis 필요)
    t = Translator(str(table_file))

    # Translator.table은 {문자: 패턴} 형태로 제공
    return dict(t.table)