#!/usr/bin/env python3
"""Append one logo item to exp4 chunk JSON, then assemble complete chunks."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
BATCHES.mkdir(exist_ok=True)


def append_item(chunk_id: str, item: dict) -> None:
    path = BATCHES / f"exp4-{chunk_id}.json"
    items = json.loads(path.read_text()) if path.exists() else []
    names = {i["name"] for i in items}
    if item["name"] not in names:
        items.append(item)
    path.write_text(json.dumps(items))
    print(f"exp4-{chunk_id}.json: {len(items)} items")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: append_exp4_item.py <chunk_id>", file=sys.stderr)
        sys.exit(1)
    chunk_id = sys.argv[1]
    item = json.load(sys.stdin)
    if isinstance(item, dict) and "data" in item:
        item = item["data"]
    append_item(chunk_id, item)


if __name__ == "__main__":
    main()
