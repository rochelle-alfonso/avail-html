#!/usr/bin/env python3
"""Merge logoId->url pairs into partner_urls.json and curl-download PNGs.

Usage:
  python3 merge_url_batch.py logoId url [logoId url ...]
  python3 merge_url_batch.py --file batch.json  # [{logoId, url}, ...]
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
manifest = {p["logoId"]: p["slug"] for p in json.loads((ROOT / "partner_manifest.json").read_text())}
OUT = ROOT / "assets" / "partners"


def merge_and_download(entries: list[tuple[str, str]]) -> None:
    urls_path = ROOT / "partner_urls.json"
    existing = {}
    if urls_path.exists():
        existing = {item["slug"]: item for item in json.loads(urls_path.read_text())}
    saved = 0
    for logo_id, url in entries:
        slug = manifest.get(logo_id)
        if not slug:
            print(f"Skip unknown logoId {logo_id}")
            continue
        existing[slug] = {"slug": slug, "url": url}
        dest = OUT / f"{slug}.png"
        if dest.exists() and dest.stat().st_size > 100:
            continue
        r = subprocess.run(["curl", "-sL", "-f", "-o", str(dest), url], capture_output=True)
        if r.returncode == 0 and dest.stat().st_size > 100:
            saved += 1
    urls_path.write_text(json.dumps(sorted(existing.values(), key=lambda x: x["slug"]), indent=2))
    total = len(list(OUT.glob("*.png")))
    print(f"Downloaded {saved} new ({total} total PNGs, {len(existing)} URLs)")


def main() -> None:
    if len(sys.argv) > 2 and sys.argv[1] == "--file":
        data = json.loads(Path(sys.argv[2]).read_text())
        entries = [(d["logoId"], d["url"]) for d in data]
    else:
        args = sys.argv[1:]
        entries = [(args[i], args[i + 1]) for i in range(0, len(args), 2)]
    merge_and_download(entries)


if __name__ == "__main__":
    main()
