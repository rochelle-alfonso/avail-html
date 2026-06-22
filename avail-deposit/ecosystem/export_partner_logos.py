#!/usr/bin/env python3
"""Export partner logos from Figma shared plugin data batches to assets/partners/."""

import base64
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
OUT = ROOT / "assets" / "partners"


def slugify(name: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))


def save_batch(data: list, batch_id: str) -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    seen: dict[str, int] = {}
    count = 0
    for item in data:
        name = item["name"]
        slug = slugify(name)
        tag = item.get("tag") or ""
        if slug in seen:
            suffix = slugify(tag) or str(seen[slug])
            slug = f"{slug}-{suffix}"
        seen[slug] = seen.get(slug, 0) + 1
        dest = OUT / f"{slug}.png"
        if not dest.exists():
            dest.write_bytes(base64.b64decode(item["b64"]))
            count += 1
    print(f"batch-{batch_id}: saved {count} new logos")
    return count


def main() -> None:
    total = 0
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            path = BATCHES / f"batch-{arg}.json"
            if path.exists():
                total += save_batch(json.loads(path.read_text()), arg)
        print(f"Done: {total} logos")
        return

    for path in sorted(BATCHES.glob("batch-*.json")):
        batch_id = path.stem.replace("batch-", "")
        total += save_batch(json.loads(path.read_text()), batch_id)
    print(f"Done: {total} logos from {len(list(BATCHES.glob('batch-*.json')))} batches")


if __name__ == "__main__":
    main()
