#!/usr/bin/env python3
"""Save one exp4 partner item from stdin to logo_batches/parts/exp4-{chunk}-{index}.json."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "logo_batches" / "parts"
PARTS.mkdir(parents=True, exist_ok=True)


def main() -> None:
    chunk, index = sys.argv[1], sys.argv[2]
    data = json.load(sys.stdin)
    path = PARTS / f"exp4-{chunk}-{index}.json"
    path.write_text(json.dumps(data))
    b64_len = len(data.get("b64") or "")
    print(f"Saved {path.name} b64={b64_len}")


if __name__ == "__main__":
    main()
