#!/usr/bin/env python3
"""
CLI: English Text ↔ Braille (unicode or dot-string)
Usage:
  $ python -m braille_converter.english.main_english -e --form unicode "Hello, 123"
  $ python -m braille_converter.english.main_english -d input.dots.txt
"""
import argparse
from .english_translator import encode, decode

def main():
    p = argparse.ArgumentParser(prog='english_braille',
        description='Convert English text ↔ Braille (Grade-1)')
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument('-e','--encode', action='store_true', help='Text → Braille')
    grp.add_argument('-d','--decode', action='store_true', help='Braille → Text')

    p.add_argument('--form', choices=['unicode','dots'], default='unicode',
                  help='braille output or input format')
    p.add_argument('data', nargs='?', help='string to convert or file path')
    p.add_argument('-f','--file', type=argparse.FileType('r'),
                   help='read input from file')

    args = p.parse_args()
    raw = args.file.read() if args.file else (args.data or input('> '))
    raw = raw.rstrip('\n')

    if args.encode:
        print(encode(raw, form=args.form))
    else:
        # if form=dots, user is providing dots; else unicode
        print(decode(raw))

if __name__ == '__main__':
    main()