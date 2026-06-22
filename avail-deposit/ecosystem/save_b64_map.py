#!/usr/bin/env python3
"""Save b64 strings from a JSON dict {index: b64} for one chunk."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
chunk = sys.argv[1]
data = json.loads(Path(sys.argv[2]).read_text())
out = ROOT / "logo_batches" / "b64"
out.mkdir(parents=True, exist_ok=True)
for idx, b64 in data.items():
    p = out / f"export-{chunk}-{idx}.txt"
    p.write_text(b64.strip())
    print(p)
