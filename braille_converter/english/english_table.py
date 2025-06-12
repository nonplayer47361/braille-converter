# Grade-1 English Braille manual base mappings

# lowercase letters a–z
LETTERS = {
    'a': '1',   'b': '12',  'c': '14',   'd': '145',  'e': '15',
    'f': '124', 'g': '1245','h': '125',  'i': '24',   'j': '245',
    'k': '13',  'l': '123', 'm': '134',  'n': '1345', 'o': '135',
    'p': '1234','q': '12345','r': '1235', 's': '234',  't': '2345',
    'u': '136', 'v': '1236','w': '2456', 'x': '1346', 'y': '13456',
    'z': '1356'
}

# capitalization indicator (dot-6)
CAPITAL_IND = '6'

# number indicator (dots 3-4-5-6)
NUMBER_IND = '3456'
# digits 1–0 map to same patterns as 'a'–'j'
NUMBERS = {
    '1': '1',  '2': '12', '3': '14',  '4': '145', '5': '15',
    '6': '124','7': '1245','8': '125','9': '24',  '0': '245'
}

# common punctuation in Grade-1
PUNCT = {
    ',': '2',   ';': '23',  ':': '25',  '.': '256',
    '?': '236', '!': '235',  '\'':'3',   '-': '36',
    '"': '356', '(': '236',  ')': '356'
}

# combine into one base mapping
BASE = {}
BASE.update(LETTERS)
BASE.update(NUMBERS)
BASE.update(PUNCT)