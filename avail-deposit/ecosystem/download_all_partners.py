#!/usr/bin/env python3
"""Fetch export URLs for all partners via Figma MCP download_assets and save PNGs.

Run in batches — append URLs to partner_urls.json, then:
  python3 download_partner_urls.py
"""

import json
import ssl
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "partner_manifest.json"
URLS = ROOT / "partner_urls.json"
OUT = ROOT / "assets" / "partners"


def download(url: str, dest: Path) -> None:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
        dest.write_bytes(resp.read())


def merge_urls(entries: list) -> None:
    existing = {}
    if URLS.exists():
        for item in json.loads(URLS.read_text()):
            existing[item["slug"]] = item
    for item in entries:
        existing[item["slug"]] = item
    out = sorted(existing.values(), key=lambda x: x["slug"])
    URLS.write_text(json.dumps(out, indent=2))
    print(f"partner_urls.json: {len(out)} entries")


def download_all() -> None:
    if not URLS.exists():
        print("No partner_urls.json — add URLs first", file=sys.stderr)
        sys.exit(1)
    OUT.mkdir(parents=True, exist_ok=True)
    items = json.loads(URLS.read_text())
    saved = 0
    for item in items:
        slug = item["slug"]
        url = item.get("url") or item.get("exportUrl")
        dest = OUT / f"{slug}.png"
        if dest.exists() and dest.stat().st_size > 100:
            continue
        if not url:
            continue
        print(f"Downloading {slug}")
        download(url, dest)
        saved += 1
    total = len(list(OUT.glob("*.png")))
    print(f"Downloaded {saved} new logos ({total} total)")


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "download"
    if cmd == "merge" and not sys.stdin.isatty():
        merge_urls(json.load(sys.stdin))
    elif cmd == "download":
        download_all()
    elif cmd == "status":
        manifest = json.loads(MANIFEST.read_text())
        have = {p.stem for p in OUT.glob("*.png")}
        urls = {u["slug"] for u in json.loads(URLS.read_text())} if URLS.exists() else set()
        print(f"manifest: {len(manifest)}  pngs: {len(have)}  urls: {len(urls)}  missing: {len(manifest)-len(have)}")
    else:
        print("Usage: download_all_partners.py [download|merge|status]")


if __name__ == "__main__":
    main()
