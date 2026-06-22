#!/usr/bin/env python3
"""Download partner logos from Figma MCP asset URLs.

Reads partner_urls.json: [{ "slug": "mayan", "url": "https://..." }, ...]
Or stdin with same format.
"""

import json
import ssl
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "partners"
URLS_FILE = ROOT / "partner_urls.json"


def download(url: str, dest: Path) -> None:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    if len(sys.argv) > 1:
        items = json.loads(Path(sys.argv[1]).read_text())
    elif not sys.stdin.isatty():
        items = json.load(sys.stdin)
    elif URLS_FILE.exists():
        items = json.loads(URLS_FILE.read_text())
    else:
        print("Usage: download_partner_urls.py [partner_urls.json]", file=sys.stderr)
        sys.exit(1)

    OUT.mkdir(parents=True, exist_ok=True)
    saved = 0
    for item in items:
        slug = item["slug"]
        url = item.get("url") or item.get("exportUrl")
        if not url:
            print(f"Skip {slug}: no url")
            continue
        dest = OUT / f"{slug}.png"
        if dest.exists() and dest.stat().st_size > 100:
            continue
        print(f"Downloading {slug}")
        download(url, dest)
        saved += 1
    print(f"Downloaded {saved} new logos ({len(list(OUT.glob('*.png')))} total)")


if __name__ == "__main__":
    main()
