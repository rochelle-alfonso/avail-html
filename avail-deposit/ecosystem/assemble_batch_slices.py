#!/usr/bin/env python3
"""Merge batch-N-*.json slice files into logo_batches/batch-N.json."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
SLICES = BATCHES / "slices"


def assemble_batch(batch_id: str) -> int:
    partner_parts = sorted(
        SLICES.glob(f"batch-{batch_id}-p*.json"),
        key=lambda p: int(p.stem.split("-p")[-1]),
    )
    slice_parts = sorted(
        p for p in SLICES.glob(f"batch-{batch_id}-*.json") if "-p" not in p.stem
    )
    parts = partner_parts or slice_parts
    if not parts:
        return 0
    items: list = []
    for part in parts:
        chunk = json.loads(part.read_text())
        if isinstance(chunk, dict):
            items.append(chunk)
        elif isinstance(chunk, list):
            items.extend(chunk)
        else:
            raise ValueError(f"{part} is not a JSON object or array")
    dest = BATCHES / f"batch-{batch_id}.json"
    dest.write_text(json.dumps(items))
    print(f"batch-{batch_id}: {len(items)} partners from {len(parts)} slices")
    return len(items)


def main() -> None:
    if len(sys.argv) > 1:
        total = sum(assemble_batch(arg) for arg in sys.argv[1:])
    else:
        total = 0
        for path in sorted(SLICES.glob("batch-*-0.json")):
            batch_id = path.stem.split("-")[1]
            total += assemble_batch(batch_id)
    print(f"Assembled {total} partners total")


if __name__ == "__main__":
    main()
