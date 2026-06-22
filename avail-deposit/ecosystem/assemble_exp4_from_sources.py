#!/usr/bin/env python3
"""Build exp4-{N}.json chunk files from all available b64 sources."""

import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
PARTNERS = ROOT / "assets" / "partners"


def b64_ok(b64: str) -> bool:
    return len(b64) > 100 and b64.endswith(
        ("QmCC", "QkCC", "ggg==", "AAA=", "CYII=", "rkJggg==")
    )


def load_manifest() -> tuple[dict[str, dict], dict[str, str]]:
    manifest = json.loads((ROOT / "partner_manifest.json").read_text())
    by_slug = {p["slug"]: p for p in manifest}
    by_name = {p["name"]: p["slug"] for p in manifest}
    return by_slug, by_name


def collect_b64() -> dict[str, str]:
    found: dict[str, str] = {}

    # b64_slugs/*.txt
    slugs_dir = BATCHES / "b64_slugs"
    for path in slugs_dir.glob("*.txt"):
        found[path.stem] = path.read_text().strip()

    # b64_cache/*.json (slug -> b64 maps)
    for path in (BATCHES / "b64_cache").glob("*.json"):
        found.update(json.loads(path.read_text()))

    # b64/export-{chunk}-{idx}.txt mapped via meta + manifest names
    _, by_name = load_manifest()
    meta_dir = BATCHES / "meta"
    b64_dir = BATCHES / "b64"
    for meta_path in sorted(meta_dir.glob("export-*.json")):
        partners = json.loads(meta_path.read_text())
        chunk = int(meta_path.stem.split("-")[1])
        for idx, partner in enumerate(partners):
            b64_path = b64_dir / f"export-{chunk}-{idx}.txt"
            if b64_path.exists():
                slug = partner.get("slug") or by_name.get(partner["name"])
                if slug:
                    found[slug] = b64_path.read_text().strip()

    # Existing exp4 chunk/part JSON
    for path in list(BATCHES.glob("exp4-*.json")) + list((BATCHES / "parts").glob("exp4-*-*.json")):
        data = json.loads(path.read_text())
        items = data if isinstance(data, list) else [data]
        for item in items:
            slug = item.get("slug")
            if not slug and "name" in item:
                from fetch_exp4_chunks import slugify

                slug = slugify(item["name"])
            if slug and item.get("b64"):
                found[slug] = item["b64"]

    # Re-encode existing PNGs as fallback
    if PARTNERS.exists():
        for png in PARTNERS.glob("*.png"):
            slug = png.stem
            if slug not in found:
                found[slug] = base64.b64encode(png.read_bytes()).decode()

    return found


def chunk_sizes() -> dict[int, int]:
    sizes = {i: 4 for i in range(36)}
    sizes[36] = 2
    return sizes


def main() -> None:
    slugs = json.loads((BATCHES / "slug_fetch_list.json").read_text())
    manifest, _ = load_manifest()
    b64_map = collect_b64()
    sizes = chunk_sizes()

    missing: list[str] = []
    truncated: list[str] = []
    written = 0

    idx = 0
    for chunk_id in range(37):
        count = sizes[chunk_id]
        items = []
        for _ in range(count):
            if idx >= len(slugs):
                break
            slug = slugs[idx]
            idx += 1
            meta = manifest.get(slug, {"name": slug, "tag": None})
            b64 = b64_map.get(slug, "")
            item = {
                "name": meta["name"],
                "tag": meta.get("tag"),
                "b64": b64,
                "slug": slug,
            }
            items.append(item)
            if not b64:
                missing.append(f"exp4-{chunk_id}: {slug}")
            elif not b64_ok(b64):
                truncated.append(f"exp4-{chunk_id}: {slug} (len={len(b64)})")

        dest = BATCHES / f"exp4-{chunk_id}.json"
        dest.write_text(json.dumps([{k: v for k, v in i.items() if k != "slug"} for i in items]))
        written += 1
        have_b64 = sum(1 for i in items if i.get("b64") and b64_ok(i["b64"]))
        print(f"exp4-{chunk_id}.json: {len(items)} items, {have_b64} with valid b64")

    print(f"\nWrote {written} chunk files")
    print(f"Missing b64: {len(missing)}")
    print(f"Truncated/invalid b64: {len(truncated)}")
    if missing[:10]:
        print("First missing:", missing[:10])
    if truncated[:10]:
        print("First truncated:", truncated[:10])


if __name__ == "__main__":
    main()
