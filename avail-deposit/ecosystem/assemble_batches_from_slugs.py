#!/usr/bin/env python3
"""Build batch-N.json from all_batches_meta.json + per-slug b64 files."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
META = ROOT / "logo_batches" / "all_batches_meta.json"
B64_DIR = ROOT / "logo_batches" / "b64_slugs"
BATCHES = ROOT / "logo_batches"


def slugify(name: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))


def logo_key(name: str, tag: str | None, seen: dict[str, int]) -> str:
    slug = slugify(name)
    if slug in seen:
        suffix = slugify(tag or "") or str(seen[slug])
        slug = f"{slug}-{suffix}"
    seen[slug] = seen.get(slug, 0) + 1
    return slug


def main() -> None:
    meta = json.loads(META.read_text())
    seen: dict[str, int] = {}
    missing: list[str] = []
    for batch_id in range(30):
        items = []
        for partner in meta[str(batch_id)]:
            key = logo_key(partner["name"], partner.get("tag"), seen)
            b64_path = B64_DIR / f"{key}.txt"
            if not b64_path.exists():
                missing.append(key)
                continue
            items.append({**partner, "b64": b64_path.read_text().strip()})
        if items:
            (BATCHES / f"batch-{batch_id}.json").write_text(json.dumps(items))
            print(f"batch-{batch_id}.json: {len(items)}/{len(meta[str(batch_id)])}")
    if missing:
        print(f"Missing b64 ({len(missing)}): {missing[:10]}...")
        sys.exit(1)


if __name__ == "__main__":
    main()
