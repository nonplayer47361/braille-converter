import json
from pathlib import Path
from functools import lru_cache

# English 빌더 임포트
from braille_converter.english.parse_liblouis_ctb import build_mapping as _build_eng
# Korean 빌더 임포트
from braille_converter.scripts.build_braille_cache import build_cache as _build_all

@lru_cache()
def load_table(lang: str) -> dict:
    """
    Load a Braille mapping table for the given language.
    lang: 'eng' or 'kor'
    Returns a dict from character/dot-pattern to mapping.
    """
    root = Path(__file__).parent.parent
    cache_dir = root / "cache"
    cache_dir.mkdir(exist_ok=True)

    eng_file = cache_dir / "eng_braille_table.json"
    kor_file = cache_dir / "kor_braille_table.json"
    # 캐시 파일이 없거나 비어 있으면 생성
    if lang == "eng" and (not eng_file.exists() or eng_file.stat().st_size == 0):
        mapping = _build_eng()
        with eng_file.open("w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
    if lang == "kor" and (not kor_file.exists() or kor_file.stat().st_size == 0):
        # build_braille_cache가 eng+kor 둘 다 생성하므로 한 번만 호출
        _build_all()
    # 해당 파일 열기
    cache_file = eng_file if lang == "eng" else kor_file
    if not cache_file.exists():
        raise FileNotFoundError(f"Braille table cache not found: {cache_file}")
    with cache_file.open(encoding="utf-8") as f:
        return json.load(f)