from .loader import load_table
from .braille_unicode_map import pattern_to_unicode, unicode_to_pattern

def text_to_braille(text: str, lang: str) -> str:
    """
    Convert plain text into a Unicode Braille string for the given language.
    Skips unmapped characters (e.g. spaces).
    """
    tbl = load_table(lang)
    out = []
    for ch in text:
        pat = tbl.get(ch)
        if not pat:
            continue
        out.append(pattern_to_unicode(pat))
    return "".join(out)

def braille_to_text(braille: str, lang: str) -> str:
    """
    Convert a Unicode Braille string back into plain text for the given language.
    Handles multi-cell patterns (e.g. capitalization or number indicators).
    """
    tbl = load_table(lang)
    # build reverse lookup: pattern -> character
    rev = {v: k for k, v in tbl.items()}
    result = []
    buf = ""
    for cell in braille:
        pat = unicode_to_pattern(cell)
        buf += pat
        if buf in rev:
            result.append(rev[buf])
            buf = ""
        elif len(buf) > 7:
            # too long, reset buffer
            buf = ""
    return "".join(result)