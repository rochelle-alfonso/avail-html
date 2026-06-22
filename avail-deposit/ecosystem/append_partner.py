#!/usr/bin/env python3
"""Append one partner record to export-{chunk}.json and save PNG."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"


def main() -> None:
    chunk = sys.argv[1]
    src = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    partner = json.loads(src.read_text()) if src else json.load(sys.stdin)
    dest = BATCHES / f"export-{chunk}.json"
    BATCHES.mkdir(parents=True, exist_ok=True)
    items = json.loads(dest.read_text()) if dest.exists() else []
    items.append(partner)
    dest.write_text(json.dumps(items))
    from save_chunk import save_items

    save_items([partner])
    print(f"Chunk {chunk}: {len(items)} partners total")


if __name__ == "__main__":
    main()
