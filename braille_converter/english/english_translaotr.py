import re
from .english_table import CAPITAL_INDICATOR, NUMERIC_INDICATOR, MAPPING, get_mapping

def encode(text: str, form: str = 'unicode') -> str:
    """
    Text → Braille
     - form='unicode' or 'dots'
     - automatically handles caps & numbers
    """
    result = []
    in_number = False

    for ch in text:
        # start number block?
        if ch.isdigit() and not in_number:
            # get_mapping will prepend indicator
            result.append(get_mapping(ch, form))
            in_number = True
            continue
        # continue number block
        if ch.isdigit() and in_number:
            result.append(get_mapping(ch, form)[len(NUMERIC_INDICATOR[form]):])
            continue

        # any other char resets number state
        in_number = False
        result.append(get_mapping(ch, form))

    return ''.join(result)

def decode(braille: str) -> str:
    """
    Braille (unicode or dots) → Text
     - detects form by checking for unicode Braille chars
     - splits into cells, reverses mapping
    """
    # detect form
    is_unicode = any('⠁' <= c <= '⣿' for c in braille)

    # split into tokens
    if is_unicode:
        cells = list(braille)
        IND_CAP = CAPITAL_INDICATOR['unicode']
        IND_NUM = NUMERIC_INDICATOR['unicode']
    else:
        IND_CAP = CAPITAL_INDICATOR['dots']
        IND_NUM = NUMERIC_INDICATOR['dots']
        # '3456' or '6', or any combination of [1-6]+
        cells = re.findall(r'3456|6|[1-6]+', braille)

    # build inverse maps
    inv: dict[str,dict[str,str]] = {'unicode':{}, 'dots':{}}
    for ch, forms in MAPPING.items():
        inv['unicode'][forms['unicode']] = ch
        inv['dots'][forms['dots']] = ch
    inv['unicode'][IND_CAP] = '<CAP>'
    inv['unicode'][IND_NUM] = '<NUM>'
    inv['dots'][IND_CAP] = '<CAP>'
    inv['dots'][IND_NUM] = '<NUM>'

    res = []
    cap = False
    num = False

    for cell in cells:
        token = inv['unicode'].get(cell) if is_unicode else inv['dots'].get(cell)
        if token == '<CAP>':
            cap = True
            continue
        if token == '<NUM>':
            num = True
            continue

        if num:
            # digit
            res.append(token)
            num = False
        else:
            # letter or punctuation
            if cap:
                token = token.upper()
                cap = False
            res.append(token)
    return ''.join(res)
    