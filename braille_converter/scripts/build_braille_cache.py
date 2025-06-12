import json
from pathlib import Path
from louis import Translator

# CTB 테이블 위치 (install_braille_ctb_files.py로 내려받은 후)
TABLE_FILES = {
    "eng": Path("braille_converter/liblouis_translator/english/en-us-g2.ctb"),
    "kor": Path("braille_converter/liblouis_translator/korean/ko-g2.ctb"),
}

def build_cache():
    out_dir = Path("braille_converter/cache")
    out_dir.mkdir(exist_ok=True)
    for lang, tbl_path in TABLE_FILES.items():
        if not tbl_path.exists():
            raise FileNotFoundError(f"테이블 파일이 없습니다: {tbl_path}")
        t = Translator(str(tbl_path))
        mapping = dict(t.table)
        with (out_dir / f"{lang}_braille_table.json").open("w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
        print(f"[+] 캐시 생성: {lang}_braille_table.json")

def main():
    build_cache()

if __name__ == "__main__":
    main()