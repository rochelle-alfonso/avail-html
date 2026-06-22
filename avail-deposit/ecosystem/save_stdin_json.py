#!/usr/bin/env python3
"""Write stdin JSON to an output path."""
import json
import sys
from pathlib import Path

out = Path(sys.argv[1])
out.parent.mkdir(parents=True, exist_ok=True)
raw = sys.stdin.read().strip()
if raw.startswith("["):
    end = raw.rfind("]")
    if end != -1:
        raw = raw[: end + 1]
data = json.loads(raw)
out.write_text(json.dumps(data))
if isinstance(data, list):
    print(f"Wrote {out} ({len(data)} items)")
    for item in data:
        b64 = item.get("b64", "")
        print(f"  {item.get('name')}: b64={len(b64)}")
else:
    b64 = data.get("b64", "")
    print(f"Wrote {out} ({data.get('name')}) b64={len(b64)}")
