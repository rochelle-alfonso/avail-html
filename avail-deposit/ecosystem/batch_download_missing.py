#!/usr/bin/env python3
"""Append download_assets export URLs for missing slugs via stdin JSON lines.

Each stdin line: {"slug": "...", "url": "..."}
Then run: python3 download_all_partners.py download
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    entries = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        entries.append(json.loads(line))
    if not entries:
        print("No entries")
        return
    proc = subprocess.run(
        [sys.executable, str(ROOT / "merge_partner_urls.py")],
        input=json.dumps(entries),
        text=True,
        capture_output=True,
    )
    print(proc.stdout.strip() or proc.stderr.strip())
    subprocess.run([sys.executable, str(ROOT / "download_all_partners.py"), "download"], check=False)


if __name__ == "__main__":
    main()
