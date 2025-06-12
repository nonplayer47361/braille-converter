#!/usr/bin/env python3
"""
Unified CLI: English + Digits + Punctuation ↔ Braille
Automatically handles unicode ↔ dots on encode/decode.
Usage:
  $ python main.py -e --form unicode "Hello! 2025"
  $ python main.py -e --form dots "Hello! 2025"
  $ python main.py -d --form unicode ⠠⠓⠑⠇⠇⠕⠖⠂⠼⠃⠚⠅⠑⠑
  $ python main.py -d --form dots 6...
"""
import argparse
from braille_converter.english.english_translator import encode, decode

def main():
    p = argparse.ArgumentParser(prog='braille',
        description='Convert mixed English+digits+punc ↔ Braille')
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument('-e','--encode', action='store_true')
    grp.add_argument('-d','--decode', action='store_true')

    p.add_argument('--form', choices=['unicode','dots'], default='unicode',
                  help='braille format for encode; ignored on decode')
    p.add_argument('data', nargs='?', help='text or braille (or file path)')
    p.add_argument('-f','--file', type=argparse.FileType('r'),
                  help='read input from file')

    args = p.parse_args()
    raw = args.file.read() if args.file else (args.data or input('> '))
    raw = raw.rstrip('\n')

    if args.encode:
        print(encode(raw, form=args.form))
    else:
        print(decode(raw))

if __name__ == '__main__':
    main()