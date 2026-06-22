#!/usr/bin/env python3
"""Save one MCP item dict to logo_batches/parts/exp4-{c}-{i}.json."""
import json
import sys
from pathlib import Path

PARTS = Path(__file__).resolve().parent / "logo_batches" / "parts"
PARTS.mkdir(parents=True, exist_ok=True)


def main() -> None:
    chunk, index, raw = sys.argv[1], sys.argv[2], sys.argv[3]
    data = json.loads(raw)
    path = PARTS / f"exp4-{chunk}-{index}.json"
    path.write_text(json.dumps(data))
    b64 = data.get("b64", "")
    print(f"Saved {path.name} ({data['name']}) b64={len(b64)}")


if __name__ == "__main__":
    main()
