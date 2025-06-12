#!/usr/bin/env python3
"""
Build a JSON braille mapping for English Grade-1:
 - letters (lower/upper)
 - digits with number indicator
 - punctuation
Outputs cache/eng_braille_table.json
"""
import json
from pathlib import Path
from braille_converter.english.english_table import BASE, LETTERS, CAPITAL_IND, NUMBER_IND

def build_mapping() -> dict:
    tbl = {}
    # lowercase letters, numbers, punctuation
    for ch, pat in BASE.items():
        tbl[ch] = pat
    # uppercase letters with capital indicator
    for ch, pat in LETTERS.items():
        tbl[ch.upper()] = CAPITAL_IND + pat
    # digits must be prefixed by number indicator at runtime;
    # but for reverse mapping we map indicator+digit-pattern -> digit
    for digit, pat in {k:v for k,v in BASE.items() if k.isdigit()}.items():
        tbl[NUMBER_IND + pat] = digit
    # build reverse mappings for all entries
    # pattern -> character
    # Note: skip number-indicator-only or capital-indicator-only patterns
    rev = {}
    for ch, pat in list(tbl.items()):
        rev[pat] = ch
    # merge both directions
    mapping = {}
    mapping.update(tbl)
    mapping.update(rev)
    return mapping

def main():
    out_dir = Path(__file__).parent.parent / "cache"
    out_dir.mkdir(parents=True, exist_ok=True)
    mapping = build_mapping()
    out_file = out_dir / "eng_braille_table.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"Wrote English braille table to {out_file}")

if __name__ == "__main__":
    main()