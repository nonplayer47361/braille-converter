# dual mapping table for Grade-1 English Braille

from typing import Literal

Form = Literal['unicode', 'dots']

CAPITAL_INDICATOR: dict[Form, str] = {
    'unicode': '⠠',
    'dots':    '6'
}
NUMERIC_INDICATOR: dict[Form, str] = {
    'unicode': '⠼',
    'dots':    '3456'
}

# a–z, 1–0, punctuation
MAPPING: dict[str, dict[Form, str]] = {
    # letters
    'a': {'unicode': '⠁', 'dots': '1'},    'b': {'unicode': '⠃', 'dots': '12'},
    'c': {'unicode': '⠉', 'dots': '14'},   'd': {'unicode': '⠙', 'dots': '145'},
    'e': {'unicode': '⠑', 'dots': '15'},   'f': {'unicode': '⠋', 'dots': '124'},
    'g': {'unicode': '⠛', 'dots': '1245'}, 'h': {'unicode': '⠓', 'dots': '125'},
    'i': {'unicode': '⠊', 'dots': '24'},   'j': {'unicode': '⠚', 'dots': '245'},
    'k': {'unicode': '⠅', 'dots': '13'},   'l': {'unicode': '⠇', 'dots': '123'},
    'm': {'unicode': '⠍', 'dots': '134'},  'n': {'unicode': '⠝', 'dots': '1345'},
    'o': {'unicode': '⠕', 'dots': '135'},  'p': {'unicode': '⠏', 'dots': '1234'},
    'q': {'unicode': '⠟', 'dots': '12345'},'r': {'unicode': '⠗', 'dots': '1235'},
    's': {'unicode': '⠎', 'dots': '234'},  't': {'unicode': '⠞', 'dots': '2345'},
    'u': {'unicode': '⠥', 'dots': '136'},  'v': {'unicode': '⠧', 'dots': '1236'},
    'w': {'unicode': '⠺', 'dots': '2456'}, 'x': {'unicode': '⠭', 'dots': '1346'},
    'y': {'unicode': '⠽', 'dots': '13456'},'z': {'unicode': '⠵', 'dots': '1356'},

    # digits (reuse a–j patterns)
    '1': {'unicode': '⠁', 'dots': '1'},   '2': {'unicode': '⠃', 'dots': '12'},
    '3': {'unicode': '⠉', 'dots': '14'},  '4': {'unicode': '⠙', 'dots': '145'},
    '5': {'unicode': '⠑', 'dots': '15'},  '6': {'unicode': '⠋', 'dots': '124'},
    '7': {'unicode': '⠛', 'dots': '1245'}, '8': {'unicode': '⠓', 'dots': '125'},
    '9': {'unicode': '⠊', 'dots': '24'},  '0': {'unicode': '⠚', 'dots': '245'},

    # punctuation & common symbols
    ',': {'unicode': '⠂', 'dots': '2'},   ';': {'unicode': '⠆', 'dots': '23'},
    ':': {'unicode': '⠒', 'dots': '25'},  '.': {'unicode': '⠲', 'dots': '256'},
    '?': {'unicode': '⠦', 'dots': '236'}, '!': {'unicode': '⠖', 'dots': '235'},
    '(': {'unicode': '⠶', 'dots': '236'}, ')': {'unicode': '⠶', 'dots': '356'},
    "'": {'unicode': '⠄', 'dots': '3'},   '-': {'unicode': '⠤', 'dots': '36'},
    '"': {'unicode': '⠶', 'dots': '356'}, '/': {'unicode': '⠌', 'dots': '456'},
    '@': {'unicode': '⠈', 'dots': '7'},   '&': {'unicode': '⠯', 'dots': '256'},
    '#': {'unicode': '⠼', 'dots': '3456'}, '*': {'unicode': '⠔', 'dots': '356'},
    '+': {'unicode': '⠖', 'dots': '235'}, '=': {'unicode': '⠶', 'dots': '236'},
}

def get_mapping(ch: str, form: Form = 'unicode') -> str:
    """
    Return the Braille cell(s) for character ch.
    - supports uppercase (prepends CAPITAL_INDICATOR)
    - supports digits (prepends NUMERIC_INDICATOR)
    - if ch not in mapping, returns ch unchanged.
    """
    out = []
    if ch.isupper():
        out.append(CAPITAL_INDICATOR[form])
        ch = ch.lower()

    if ch.isdigit():
        out.append(NUMERIC_INDICATOR[form])
        out.append(MAPPING.get(ch, {form: ch})[form])
    else:
        out.append(MAPPING.get(ch, {form: ch})[form])

    return ''.join(out)

# Expose the “dots”-based tables that parse_liblouis_ctb.py expects:
BASE = {ch: specs['dots'] for ch, specs in MAPPING.items()}
LETTERS = {ch: specs['dots'] for ch, specs in MAPPING.items() if ch.isalpha()}
CAPITAL_IND = CAPITAL_INDICATOR['dots']
NUMBER_IND = NUMERIC_INDICATOR['dots']