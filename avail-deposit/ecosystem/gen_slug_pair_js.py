#!/usr/bin/env python3
"""Generate use_figma JS to fetch logo b64 for slug pairs from slug_pairs.json."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAIRS = ROOT / "logo_batches" / "slug_pairs.json"


def js_for_pair(slugs: list[str]) -> str:
    inner = ", ".join(f"'{s}'" for s in slugs)
    return (
        f"const slugs = [{inner}];\n"
        "const out = {};\n"
        "for (const s of slugs) {\n"
        "  out[s] = figma.root.getSharedPluginData('ecosystem', `logo-${s}`);\n"
        "}\n"
        "return out;"
    )


def main() -> None:
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    pairs = json.loads(PAIRS.read_text())
    for i, slugs in enumerate(pairs[start : start + count]):
        print(f"PAIR {start + i}: {slugs}")
        print(js_for_pair(slugs))
        print("---")


if __name__ == "__main__":
    main()
