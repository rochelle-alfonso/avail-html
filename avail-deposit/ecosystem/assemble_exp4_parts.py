#!/usr/bin/env python3
"""Assemble logo_batches/parts/exp4-{chunk}-*.json into exp4-{chunk}.json."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
PARTS = BATCHES / "parts"


def assemble(chunk: int) -> int:
    files = sorted(PARTS.glob(f"exp4-{chunk}-*.json"), key=lambda p: int(p.stem.rsplit("-", 1)[-1]))
    if not files:
        return 0
    items = [json.loads(p.read_text()) for p in files]
    dest = BATCHES / f"exp4-{chunk}.json"
    dest.write_text(json.dumps(items))
    print(f"Assembled {dest.name} ({len(items)} items)")
    return len(items)


def main() -> None:
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            assemble(int(arg))
        return
    for chunk in range(37):
        assemble(chunk)


if __name__ == "__main__":
    main()
