#!/usr/bin/env python3
"""Fetch all missing slug pairs from Figma and save PNGs.

Runs use_figma via subprocess calling the Cursor MCP is not available;
instead this script saves slug maps from b64_cache and reports missing pairs.
Use with agent loop: agent fetches pairs, writes JSON to b64_cache/pair_NN.json, then runs this.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAIRS = ROOT / "logo_batches" / "slug_pairs.json"
OUT = ROOT / "assets" / "partners"
CACHE = ROOT / "logo_batches" / "b64_cache"


def existing_slugs() -> set[str]:
    return {p.stem for p in OUT.glob("*.png")}


def missing_pairs() -> list[tuple[int, list[str]]]:
    pairs = json.loads(PAIRS.read_text())
    have = existing_slugs()
    out = []
    for i, pair in enumerate(pairs):
        if any(s not in have for s in pair):
            out.append((i, pair))
    return out


def flush_cache() -> None:
    subprocess.run([sys.executable, str(ROOT / "flush_b64_cache.py")], check=True)


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        missing = missing_pairs()
        print(f"PNG count: {len(list(OUT.glob('*.png')))}")
        print(f"Missing pairs: {len(missing)}/71")
        for i, p in missing[:30]:
            print(f"  {i}: {p}")
        if len(missing) > 30:
            print(f"  ... {len(missing) - 30} more")
    elif cmd == "flush":
        flush_cache()
        print(f"PNG count: {len(list(OUT.glob('*.png')))}")
    elif cmd == "mcp-code":
        idx = int(sys.argv[2])
        pair = json.loads(PAIRS.read_text())[idx]
        slugs_js = json.dumps(pair)
        print(
            f"const slugs = {slugs_js};\n"
            "const out = {};\n"
            "for (const s of slugs) {\n"
            "  out[s] = figma.root.getSharedPluginData('ecosystem', `logo-${s}`);\n"
            "}\n"
            "return out;"
        )
    else:
        raise SystemExit(f"Unknown: {cmd}")


if __name__ == "__main__":
    main()
