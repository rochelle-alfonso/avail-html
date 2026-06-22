#!/usr/bin/env python3
"""Save a JSON array of b64 strings to per-partner .txt files."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
chunk = sys.argv[1]
start = int(sys.argv[2])
arr = json.load(sys.stdin)
out_dir = ROOT / "logo_batches" / "b64"
out_dir.mkdir(parents=True, exist_ok=True)
for i, b64 in enumerate(arr):
    p = out_dir / f"export-{chunk}-{start + i}.txt"
    p.write_text(b64.strip())
    print(p)
print(f"Saved {len(arr)} b64 for chunk {chunk} start {start}")
