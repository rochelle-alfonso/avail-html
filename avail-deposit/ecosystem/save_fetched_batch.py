#!/usr/bin/env python3
"""Save a batch of fetched MCP items to logo_batches/parts/."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "logo_batches" / "parts"
PARTS.mkdir(parents=True, exist_ok=True)


def main() -> None:
    batch = json.loads(Path(sys.argv[1]).read_text())
    for entry in batch:
        chunk = entry["chunk"]
        index = entry["index"]
        item = entry["item"]
        path = PARTS / f"exp4-{chunk}-{index}.json"
        path.write_text(json.dumps(item))
        b64_len = len(item.get("b64") or "")
        ends = (item.get("b64") or "")[-8:]
        print(f"Saved {path.name} b64={b64_len} ends={ends}")


if __name__ == "__main__":
    main()
