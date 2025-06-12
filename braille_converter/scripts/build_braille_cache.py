@lru_cache()
def load_table(lang: str) -> dict:
    cache_file = Path(__file__).parent.parent / "cache" / f"{lang}_braille_table.json"
    if not cache_file.exists():
        raise FileNotFoundError(f"Braille table cache not found: {cache_file}")
    return json.load(cache_file.open(encoding="utf-8"))