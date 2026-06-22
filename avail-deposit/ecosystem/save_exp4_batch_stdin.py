#!/usr/bin/env python3
"""Save batched exp4 partner items from stdin.

Input: [{\"c\": 0, \"i\": 0, \"item\": {\"name\": ..., \"tag\": ..., \"b64\": ...}}, ...]
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "logo_batches" / "parts"
PARTS.mkdir(parents=True, exist_ok=True)


def main() -> None:
    data = json.load(sys.stdin)
    for entry in data:
        c, i, item = entry["c"], entry["i"], entry["item"]
        path = PARTS / f"exp4-{c}-{i}.json"
        path.write_text(json.dumps(item))
        print(f"Saved exp4-{c}-{i}.json b64={len(item.get('b64') or '')}")


if __name__ == "__main__":
    main()
