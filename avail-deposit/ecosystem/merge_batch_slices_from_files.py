#!/usr/bin/env python3
"""Merge batch slice JSON files into batch-N.json and export PNGs."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
SLICES = BATCHES / "batch_slices"


def merge_batch(batch_id: int) -> int:
    parts = sorted(SLICES.glob(f"batch-{batch_id}-*.json"))
    if not parts:
        return 0
    items = []
    for p in parts:
        items.extend(json.loads(p.read_text()))
    (BATCHES / f"batch-{batch_id}.json").write_text(json.dumps(items))
    return len(items)


def main() -> None:
    SLICES.mkdir(parents=True, exist_ok=True)
    if len(sys.argv) > 1:
        ids = [int(x) for x in sys.argv[1:]]
    else:
        ids = sorted({int(p.name.split("-")[1]) for p in SLICES.glob("batch-*-*.json")})
    total = 0
    for bid in ids:
        n = merge_batch(bid)
        if n:
            print(f"batch-{bid}.json: {n} items")
            total += n
    if total:
        subprocess.run([sys.executable, str(ROOT / "export_partner_logos.py")], check=True)
    count = len(list((ROOT / "assets" / "partners").glob("*.png")))
    print(f"PNG count: {count}")


if __name__ == "__main__":
    main()
