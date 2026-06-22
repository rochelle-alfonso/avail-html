#!/usr/bin/env python3
"""Save all exp4-*.json chunk files from logo_batches/ to assets/partners/."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
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
            suffix = slugify(tag) or str(seen[slug])
            slug = f"{slug}-{suffix}"
        seen[slug] = seen.get(slug, 0) + 1
        dest = OUT / f"{slug}.png"
        if item.get("b64") and len(item["b64"]) > 100:
            import base64

            dest.write_bytes(base64.b64decode(item["b64"]))
            saved += 1
    return saved


def main() -> None:
    chunks = sorted(BATCHES.glob("exp4-*.json"), key=lambda p: int(p.stem.split("-")[1]))
    if not chunks:
        print("No exp4-*.json files found", file=sys.stderr)
        sys.exit(1)
    total = 0
    for chunk in chunks:
        items = json.loads(chunk.read_text())
        n = save_items(items)
        print(f"{chunk.name}: saved {n}")
        total += n
    print(f"Total PNG files: {len(list(OUT.glob('*.png')))}")


if __name__ == "__main__":
    main()
