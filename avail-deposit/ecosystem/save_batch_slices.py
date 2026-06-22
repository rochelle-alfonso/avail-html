#!/usr/bin/env python3
"""Save multi-batch slice payload from Figma MCP to logo_batches/slices/."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SLICES = ROOT / "logo_batches" / "slices"


def main() -> None:
    payload = json.load(sys.stdin)
    if isinstance(payload, list):
        # single slice array — requires batch id + slice id args
        if len(sys.argv) < 3:
            raise SystemExit("Usage: save_batch_slices.py <batch-id> <slice-id>  (array stdin)")
        dest = SLICES / f"batch-{sys.argv[1]}-{sys.argv[2]}.json"
        SLICES.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(payload))
        print(dest)
        return

    SLICES.mkdir(parents=True, exist_ok=True)
    for key, data in payload.items():
        if "-" not in key:
            continue
        batch_id, slice_id = key.split("-", 1)
        dest = SLICES / f"batch-{batch_id}-{slice_id}.json"
        dest.write_text(json.dumps(data))
        print(dest)


if __name__ == "__main__":
    main()
