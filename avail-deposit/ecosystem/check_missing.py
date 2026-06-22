#!/usr/bin/env python3
"""Generate shell script to fetch Figma export URLs via MCP download_assets batches."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "partner_manifest.json").read_text())
have = {p.stem for p in (ROOT / "assets/partners").glob("*.png")}
missing = [p for p in manifest if p["slug"] not in have]
print(f"missing {len(missing)} of {len(manifest)}")
for i, p in enumerate(missing[:20]):
    print(f"  {p['slug']}: {p['logoId']}")
