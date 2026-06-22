#!/usr/bin/env python3
"""Assemble export-{chunk}.json from meta + per-partner b64 files."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
META = BATCHES / "meta"
B64 = BATCHES / "b64"


def assemble_chunk(chunk: int) -> int:
    meta_path = META / f"export-{chunk}.json"
    if not meta_path.exists():
        print(f"Missing meta {meta_path}")
        return 0
    meta = json.loads(meta_path.read_text())
    partners = []
    for i, m in enumerate(meta):
        b64_path = B64 / f"export-{chunk}-{i}.txt"
        if not b64_path.exists():
            print(f"Missing b64 {b64_path}")
            return 0
        partners.append({**m, "b64": b64_path.read_text().strip()})
    dest = BATCHES / f"export-{chunk}.json"
    dest.write_text(json.dumps(partners))
    subprocess.run(
        [sys.executable, str(ROOT / "save_chunk.py"), str(dest)],
        check=True,
    )
    return len(partners)


def main() -> None:
    META.mkdir(parents=True, exist_ok=True)
    B64.mkdir(parents=True, exist_ok=True)
    total = 0
    for chunk in range(19):
        n = assemble_chunk(chunk)
        if n:
            print(f"Chunk {chunk}: {n} partners")
            total += n
    count = len(list((ROOT / "assets" / "partners").glob("*.png")))
    print(f"PNG files: {count}")


if __name__ == "__main__":
    main()
