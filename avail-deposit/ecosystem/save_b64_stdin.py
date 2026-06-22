#!/usr/bin/env python3
"""Save b64 text from stdin to logo_batches/b64/export-{chunk}-{index}.txt"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
out = ROOT / "logo_batches" / "b64" / f"export-{sys.argv[1]}-{sys.argv[2]}.txt"
out.parent.mkdir(parents=True, exist_ok=True)
data = sys.stdin.read().strip()
out.write_text(data)
print(out)
