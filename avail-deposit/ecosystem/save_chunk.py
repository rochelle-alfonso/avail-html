#!/usr/bin/env python3
"""Save partner PNGs from a JSON chunk file (from Figma export-N or batch-N)."""

import base64
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "partners"


def slugify(name: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))


def save_items(items: list) -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    seen: dict[str, int] = {}
    saved = 0
    for item in items:
        name = item["name"]
        tag = item.get("tag") or ""
        slug = slugify(name)
        if slug in seen:
            slug = f"{slug}-{slugify(tag) or seen[slug]}"
        seen[slug] = seen.get(slug, 0) + 1
        dest = OUT / f"{slug}.png"
        if not dest.exists():
            dest.write_bytes(base64.b64decode(item["b64"]))
            saved += 1
    return saved


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if path and path.exists():
        items = json.loads(path.read_text())
    else:
        items = json.load(sys.stdin)
    count = save_items(items)
    print(f"Saved {count} new logos ({len(items)} in chunk)")


if __name__ == "__main__":
    main()
