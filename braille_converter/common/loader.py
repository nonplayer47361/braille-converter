import json
from pathlib import Path
from functools import lru_cache

@lru_cache()
def load_table(lang: str) -> dict:
    """
    Load a Braille mapping table for the given language.
    lang: 'eng' or 'kor'
    Returns a dict from character/dot-pattern to mapping.
    """
    cache_file = (
        Path(__file__).parent.parent
        / "cache"
        / f"{lang}_braille_table.json"
    )
    if not cache_file.exists():
        raise FileNotFoundError(f"Braille table cache not found: {cache_file}")
    with cache_file.open(encoding="utf-8") as f:
        return json.load(f)