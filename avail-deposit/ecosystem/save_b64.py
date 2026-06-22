#!/usr/bin/env python3
"""Save one b64 string to logo_batches/b64/export-{chunk}-{index}.txt"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
chunk, idx = sys.argv[1], sys.argv[2]
b64 = sys.argv[3] if len(sys.argv) > 3 else sys.stdin.read().strip()
out = ROOT / "logo_batches" / "b64" / f"export-{chunk}-{idx}.txt"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(b64)
print(out)
