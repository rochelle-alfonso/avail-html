#!/usr/bin/env python3
"""Fetch all batch-N.json files from saved slice files and run export.

Slice files live in logo_batches/slices/batch-{N}-{S}.json
Use Figma MCP with:
  const b = JSON.parse(figma.root.getSharedPluginData('ecosystem', 'batch-N'));
  return b.slice(START, END);

Batch layout (from meta probe): batches 0-28 have 5 partners; batch 29 has 1.
Recommended slices per batch: slice-0 = [0:3], slice-1 = [3:5]; batch-29 = [0:1] only.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
SLICES = BATCHES / "slices"


def assemble_all() -> list[int]:
    missing = []
    for batch_id in range(30):
        parts = sorted(SLICES.glob(f"batch-{batch_id}-*.json"))
        if not parts:
            if batch_id != 0 or not (BATCHES / "batch-0.json").exists():
                missing.append(batch_id)
            continue
        items = []
        for part in parts:
            items.extend(__import__("json").loads(part.read_text()))
        (BATCHES / f"batch-{batch_id}.json").write_text(__import__("json").dumps(items))
        print(f"batch-{batch_id}.json: {len(items)} partners")
    return missing


def main() -> None:
    missing = assemble_all()
    if missing:
        print(f"Missing batches (no slices): {missing}")
    subprocess.run([sys.executable, str(ROOT / "export_partner_logos.py")], check=True)
    count = len(list((ROOT / "assets" / "partners").glob("*.png")))
    print(f"PNG count: {count}")


if __name__ == "__main__":
    main()
