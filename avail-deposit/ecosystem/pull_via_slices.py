#!/usr/bin/env python3
"""Pull full export chunks from Figma via use_figma MCP and save PNGs.

Usage: run slices via MCP, save JSON to logo_batches/slices/export-{c}-{s}.json,
then: python3 pull_via_slices.py

Or save partial chunk files as logo_batches/export-{c}.json and run save_chunk.py.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
SLICES = BATCHES / "slices"
META = BATCHES / "meta"


def meta_sizes() -> list[int]:
    return [len(json.loads((META / f"export-{c}.json").read_text())) for c in range(19)]


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


def assemble_and_save() -> None:
    subprocess.run([sys.executable, str(ROOT / "assemble_from_b64.py")], check=True)


def save_partial_chunks() -> int:
    """Merge any exp*-*.json or partial export files via save_chunk."""
    saved = 0
    for path in sorted(BATCHES.glob("exp*.json")):
        subprocess.run(
            [sys.executable, str(ROOT / "save_chunk.py"), str(path)],
            check=True,
        )
        saved += 1
    for path in sorted(BATCHES.glob("export-*.json")):
        subprocess.run(
            [sys.executable, str(ROOT / "save_chunk.py"), str(path)],
            check=True,
        )
        saved += 1
    return saved


def main() -> None:
    SLICES.mkdir(parents=True, exist_ok=True)
    applied = 0
    for chunk, n in enumerate(meta_sizes()):
        for start in range(0, n, 2):
            if apply_slice(chunk, start):
                applied += 1
    if applied:
        assemble_and_save()
    else:
        save_partial_chunks()
    count = len(list((ROOT / "assets" / "partners").glob("*.png")))
    print(f"PNG count: {count}")


if __name__ == "__main__":
    main()
