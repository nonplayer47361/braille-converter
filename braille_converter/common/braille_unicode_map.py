# Converts between dot-pattern strings (e.g. "145") and Unicode Braille characters.

def pattern_to_unicode(pattern: str) -> str:
    """
    Convert a string of digits '1'..'6' into a single Unicode Braille character.
    Dots are numbered:
      1 4
      2 5
      3 6
    """
    bits = 0
    for ch in pattern:
        idx = int(ch) - 1
        bits |= 1 << idx
    return chr(0x2800 + bits)

def unicode_to_pattern(ch: str) -> str:
    """
    Convert a single Unicode Braille character into its dot-pattern string.
    Returns digits '1'..'6' in ascending order.
    """
    code = ord(ch) - 0x2800
    pattern = ""
    for i in range(6):
        if code & (1 << i):
            pattern += str(i + 1)
    return pattern