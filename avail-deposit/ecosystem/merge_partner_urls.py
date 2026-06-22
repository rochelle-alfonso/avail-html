#!/usr/bin/env python3
"""Merge download URL entries into partner_urls.json."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
URLS = ROOT / "partner_urls.json"


def main() -> None:
    new_items = json.loads(sys.stdin.read())
    if isinstance(new_items, dict):
        new_items = [new_items]
    existing = {}
    if URLS.exists():
        for item in json.loads(URLS.read_text()):
            existing[item["slug"]] = item
    for item in new_items:
        existing[item["slug"]] = item
    out = list(existing.values())
    out.sort(key=lambda x: x["slug"])
    URLS.write_text(json.dumps(out, indent=2))
    print(f"partner_urls.json: {len(out)} entries")


if __name__ == "__main__":
    main()
