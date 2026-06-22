#!/usr/bin/env python3
"""Report missing slug pairs and PNG count."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAIRS = ROOT / "logo_batches" / "slug_pairs.json"
OUT = ROOT / "assets" / "partners"
B64 = ROOT / "logo_batches" / "b64_slugs"


def main() -> None:
    pairs = json.loads(PAIRS.read_text())
    existing = {p.stem for p in OUT.glob("*.png")}
    b64 = {p.stem for p in B64.glob("*.txt")}
    have = existing | b64
    all_slugs = []
    for pair in pairs:
        all_slugs.extend(pair)
    missing = sorted({s for s in all_slugs if s not in have})
    print(f"PNG files: {len(existing)}")
    print(f"b64_slugs: {len(b64)}")
    print(f"Missing slugs ({len(missing)}):")
    for s in missing:
        print(s)


if __name__ == "__main__":
    main()
