#!/usr/bin/env python3
"""
Interactive CLI: English Text ↔ Braille (unicode or dot-string)
이제 실행 시 플래그 없이 터미널에서 바로 모드를 선택하고, 입력을 받고, 결과를 출력합니다.
"""
import sys
import re
from braille_converter.english.english_table import CAPITAL_INDICATOR, NUMERIC_INDICATOR, MAPPING, get_mapping
from braille_converter.english.english_translator import encode, decode

def prompt_mode() -> str:
    while True:
        choice = input("모드를 선택하세요 – [E]ncode, [D]ecode, [Q]uit: ").strip().lower()
        if choice in ('e', 'encode'): return 'encode'
        if choice in ('d', 'decode'): return 'decode'
        if choice in ('q', 'quit'): sys.exit(0)
        print("올바른 값을 입력하세요: E, D 또는 Q.")

def prompt_form() -> str:
    while True:
        form = input("출력 형식 선택 – unicode 또는 dots: ").strip().lower()
        if form in ('unicode', 'dots'): return form
        print("‘unicode’ 또는 ‘dots’ 중 하나를 입력하세요.")

def interactive():
    print("영문 텍스트 ↔ 점자 변환기 (인터랙티브 모드)\n")
    while True:
        mode = prompt_mode()
        if mode == 'encode':
            form = prompt_form()
            src = input("변환할 텍스트를 입력하세요: ")
            print("\n→ 결과 점자:")
            print(encode(src, form=form))
        else:  # decode
            src = input("복원할 점자(유니코드 또는 dots) 를 입력하세요: ")
            print("\n→ 원문 텍스트:")
            print(decode(src))
        print("\n---\n")

if __name__ == '__main__':
    try:
        interactive()
    except (EOFError, KeyboardInterrupt):
        print("\n종료합니다.")
        sys.exit(0)