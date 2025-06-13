import re
from .english_table import CAPITAL_INDICATOR, NUMERIC_INDICATOR, MAPPING, get_mapping

def encode(text: str, form: str = 'unicode') -> str:
    result = []
    in_number = False
    for ch in text:
        if ch.isdigit() and not in_number:
            result.append(get_mapping(ch, form))
            in_number = True
            continue
        if ch.isdigit() and in_number:
            # 앞의 NUMERIC_INDICATOR[form] 길이를 제거하고 매핑만 추가
            cell = get_mapping(ch, form)
            result.append(cell[len(NUMERIC_INDICATOR[form]):])
            continue
        in_number = False
        result.append(get_mapping(ch, form))
    return ''.join(result)

def decode(braille: str) -> str:
    is_unicode = any('⠁' <= c <= '⣿' for c in braille)
    if is_unicode:
        cells = list(braille)
        IND_CAP = CAPITAL_INDICATOR['unicode']
        IND_NUM = NUMERIC_INDICATOR['unicode']
    else:
        IND_CAP = CAPITAL_INDICATOR['dots']
        IND_NUM = NUMERIC_INDICATOR['dots']
        cells = re.findall(r'3456|6|[1-6]+', braille)

    inv = {'unicode':{}, 'dots':{}}
    for ch, forms in MAPPING.items():
        inv['unicode'][forms['unicode']] = ch
        inv['dots'][forms['dots']]       = ch
    inv['unicode'][IND_CAP] = '<CAP>'
    inv['unicode'][IND_NUM] = '<NUM>'
    inv['dots'][IND_CAP]    = '<CAP>'
    inv['dots'][IND_NUM]    = '<NUM>'

    res = []
    cap = num = False
    key = 'unicode' if is_unicode else 'dots'
    for cell in cells:
        tok = inv[key].get(cell)
        if tok == '<CAP>':
            cap = True
            continue
        if tok == '<NUM>':
            num = True
            continue
        if num:
            res.append(tok)
            num = False
        else:
            if cap:
                tok = tok.upper()
                cap = False
            res.append(tok)
    return ''.join(res)