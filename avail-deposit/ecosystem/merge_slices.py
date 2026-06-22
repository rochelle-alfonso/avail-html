#!/usr/bin/env python3
"""Merge slice files into logo_batches/export-{i}.json and run save_chunk."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SLICES = ROOT / "logo_batches" / "slices"
OUT = ROOT / "logo_batches"


def merge_chunk(i: int) -> int:
    parts: list = []
    for start in (0, 2, 4, 6):
        if i == 18 and start >= 2:
            break
        path = SLICES / f"export-{i}-{start}.json"
        if not path.exists():
            print(f"Missing slice {path}")
            return 0
        parts.extend(json.loads(path.read_text()))
    dest = OUT / f"export-{i}.json"
    dest.write_text(json.dumps(parts))
    return len(parts)


def main() -> None:
    SLICES.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for i in range(19):
        n = merge_chunk(i)
        if n:
            subprocess.run(
                [sys.executable, str(ROOT / "save_chunk.py"), str(OUT / f"export-{i}.json")],
                check=True,
            )
            total += n
            print(f"Chunk {i}: {n} partners")
    count = len(list((ROOT / "assets" / "partners").glob("*.png")))
    print(f"PNG files in assets/partners: {count}")


if __name__ == "__main__":
    main()
