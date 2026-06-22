#!/usr/bin/env python3
"""Save a JSON array slice from stdin to logo_batches/slices/batch-{N}-{S}.json."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SLICES = ROOT / "logo_batches" / "slices"


def main() -> None:
    batch_id, slice_id = sys.argv[1], sys.argv[2]
    data = json.load(sys.stdin)
    SLICES.mkdir(parents=True, exist_ok=True)
    dest = SLICES / f"batch-{batch_id}-{slice_id}.json"
    dest.write_text(json.dumps(data))
    print(f"{dest} ({len(data)} items)")


if __name__ == "__main__":
    main()
