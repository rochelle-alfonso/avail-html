#!/usr/bin/env python3
"""Fetch all partner b64 via use_figma MCP slices and assemble PNGs.

Run from ecosystem dir. Requires FIGMA_ACCESS_TOKEN or uses MCP externally.
This script saves b64 slices when given slice JSON files in logo_batches/slices/.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SLICES = ROOT / "logo_batches" / "slices"
B64 = ROOT / "logo_batches" / "b64"
META = ROOT / "logo_batches" / "meta"


def apply_slice(chunk: int, start: int) -> bool:
    src = SLICES / f"export-{chunk}-{start}.json"
    if not src.exists():
        return False
    subprocess.run(
        [sys.executable, str(ROOT / "save_b64_array_stdin.py"), str(chunk), str(start)],
        input=src.read_text(),
        text=True,
        check=True,
    )
    return True


def chunk_sizes() -> list[int]:
    sizes = []
    for c in range(19):
        meta = json.loads((META / f"export-{c}.json").read_text())
        sizes.append(len(meta))
    return sizes


def main() -> None:
    SLICES.mkdir(parents=True, exist_ok=True)
    B64.mkdir(parents=True, exist_ok=True)
    sizes = chunk_sizes()
    applied = 0
    for chunk, n in enumerate(sizes):
        for start in range(0, n, 2):
            if apply_slice(chunk, start):
                applied += 1
    print(f"Applied {applied} slices")
    subprocess.run([sys.executable, str(ROOT / "assemble_from_b64.py")], check=True)


if __name__ == "__main__":
    main()
