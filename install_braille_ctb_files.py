#!/usr/bin/env python3
"""
install_braille_ctb_files.py

Fetches upstream liblouis CTB/CTI tables and installs them under
braille_converter/liblouis_translator/{common,english,korean}.
"""

import sys
from pathlib import Path

import requests

# Map of relative destination → upstream URL
TABLES = {
    # common (patterns)
    "common/braille-patterns.cti": (
        "https://raw.githubusercontent.com/liblouis/liblouis/master/tables/"
        "braille-patterns.cti"
    ),
    # english (grade‐1 and grade‐2)
    "english/en-us-g1.ctb": (
        "https://raw.githubusercontent.com/liblouis/liblouis/master/tables/"
        "en-us-g1.ctb"
    ),
    "english/en-us-g2.ctb": (
        "https://raw.githubusercontent.com/liblouis/liblouis/master/tables/"
        "en-us-g2.ctb"
    ),
    # korean (CTI and CTB)
    "korean/ko-chars.cti": (
        "https://raw.githubusercontent.com/liblouis/liblouis/master/tables/"
        "ko-chars.cti"
    ),
    "korean/ko-g1-rules.cti": (
        "https://raw.githubusercontent.com/liblouis/liblouis/master/tables/"
        "ko-g1-rules.cti"
    ),
    "korean/ko-g1.ctb": (
        "https://raw.githubusercontent.com/liblouis/liblouis/master/tables/"
        "ko-g1.ctb"
    ),
    "korean/ko-g2-rules.cti": (
        "https://raw.githubusercontent.com/liblouis/liblouis/master/tables/"
        "ko-g2-rules.cti"
    ),
    "korean/ko-g2.ctb": (
        "https://raw.githubusercontent.com/liblouis/liblouis/master/tables/"
        "ko-g2.ctb"
    ),
    "korean/ko.cti": (
        "https://raw.githubusercontent.com/liblouis/liblouis/master/tables/"
        "ko.cti"
    ),
}

def download_and_write(url: str, dest: Path) -> bool:
    """Download URL and write it to dest. Return True on success."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"ERROR: failed to download {url}: {e}", file=sys.stderr)
        return False
    dest.write_bytes(resp.content)
    return True

def main():
    root = Path(__file__).parent
    base = root / "braille_converter" / "liblouis_translator"

    print("Installing liblouis tables...")
    for rel_path, url in TABLES.items():
        dest_path = base / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"  → {rel_path}")
        if not download_and_write(url, dest_path):
            print(f"    ✗ failed to install {rel_path}", file=sys.stderr)
        else:
            print(f"    ✓ installed")

    print("\nInstallation complete.")

if __name__ == "__main__":
    main()