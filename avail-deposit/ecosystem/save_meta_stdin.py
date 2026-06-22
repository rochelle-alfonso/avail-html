#!/usr/bin/env python3
"""Save meta JSON from stdin to logo_batches/meta/export-{chunk}.json"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
out = ROOT / "logo_batches" / "meta" / f"export-{sys.argv[1]}.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(json.load(sys.stdin)))
print(f"Saved meta -> {out}")
