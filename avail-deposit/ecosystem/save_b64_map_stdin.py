#!/usr/bin/env python3
"""Save partner PNGs from {slug: b64, ...} JSON object."""

import base64
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "assets" / "partners"


def main() -> None:
    data = json.loads(sys.stdin.read())
    OUT.mkdir(parents=True, exist_ok=True)
    saved = 0
    for slug, b64 in data.items():
        if not b64 or len(b64) < 100:
            print(f"Skip {slug}: empty b64")
            continue
        dest = OUT / f"{slug}.png"
        dest.write_bytes(base64.b64decode(b64))
        saved += 1
    print(f"Saved {saved} logos ({len(list(OUT.glob('*.png')))} total)")


if __name__ == "__main__":
    main()
