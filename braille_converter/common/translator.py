import re
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
            buf = ""
    return "".join(result)

def text_to_braille_alpha(text: str, lang: str) -> str:
    """
    영문자(A–Z, a–z)만 남기고 나머지(숫자·특수·공백)는 제거한 뒤 점자로 변환.
    """
    filtered = re.sub(r"[^A-Za-z]", "", text)
    return text_to_braille(filtered, lang)

def text_to_braille_num_special(text: str, lang: str) -> str:
    """
    숫자(0–9)와 특수문자만 남기고 나머지(영문·공백)는 제거한 뒤 점자로 변환.
    """
    filtered = re.sub(r"[A-Za-z\s]", "", text)
    return text_to_braille(filtered, lang)