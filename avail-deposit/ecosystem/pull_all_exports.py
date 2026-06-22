#!/usr/bin/env python3
"""Save all export-N.json chunk files from logo_batches/ to assets/partners/."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"


def main() -> None:
    chunks = sorted(BATCHES.glob("export-*.json"), key=lambda p: int(p.stem.split("-")[1]))
    if not chunks:
        print("No export-*.json files in logo_batches/", file=sys.stderr)
        sys.exit(1)
    total = 0
    for chunk in chunks:
        result = subprocess.run(
            [sys.executable, str(ROOT / "save_chunk.py"), str(chunk)],
            capture_output=True,
            text=True,
        )
        print(result.stdout.strip())
        if result.returncode:
            print(result.stderr, file=sys.stderr)
            sys.exit(result.returncode)
        total += 1
    partners = list((ROOT / "assets" / "partners").glob("*.png"))
    print(f"Done: {total} chunks, {len(partners)} PNG files")


if __name__ == "__main__":
    main()
