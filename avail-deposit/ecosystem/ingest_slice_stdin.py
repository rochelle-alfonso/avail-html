#!/usr/bin/env python3
"""Read JSON b64 array from stdin, save slice file and per-partner .txt files."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
chunk, start = sys.argv[1], sys.argv[2]
arr = json.load(sys.stdin)
SLICES = ROOT / "logo_batches" / "slices"
SLICES.mkdir(parents=True, exist_ok=True)
(SLICES / f"export-{chunk}-{start}.json").write_text(json.dumps(arr))
subprocess.run(
    [sys.executable, str(ROOT / "save_b64_array_stdin.py"), chunk, start],
    input=json.dumps(arr),
    text=True,
    check=True,
)
