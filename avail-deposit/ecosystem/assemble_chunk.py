#!/usr/bin/env python3
"""Merge partner JSON arrays into logo_batches/export-{index}.json."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "logo_batches"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: assemble_chunk.py CHUNK_INDEX [json_file ...]")
        sys.exit(1)
    chunk_idx = sys.argv[1]
    items: list = []
    if len(sys.argv) > 2:
        for path in sys.argv[2:]:
            items.extend(json.loads(Path(path).read_text()))
    else:
        for line in sys.stdin:
            line = line.strip()
            if line:
                data = json.loads(line)
                if isinstance(data, list):
                    items.extend(data)
                else:
                    items.append(data)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dest = OUT_DIR / f"export-{chunk_idx}.json"
    dest.write_text(json.dumps(items))
    print(f"Wrote {dest} ({len(items)} partners)")


if __name__ == "__main__":
    main()
