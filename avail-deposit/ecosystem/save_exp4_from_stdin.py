#!/usr/bin/env python3
"""Save exp4 chunk JSON from stdin to logo_batches/exp4-{id}.json."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
BATCHES.mkdir(exist_ok=True)


def main() -> None:
    chunk_id = sys.argv[1] if len(sys.argv) > 1 else "0"
    data = json.load(sys.stdin)
    if isinstance(data, dict) and "data" in data:
        data = data["data"]
    path = BATCHES / f"exp4-{chunk_id}.json"
    path.write_text(json.dumps(data))
    print(f"Saved {path.name} ({len(data)} items)")


if __name__ == "__main__":
    main()
