#!/usr/bin/env python3
"""Generate use_figma JS for slug b64 groups and report fetch progress."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GROUPS = ROOT / "logo_batches" / "slug_groups.json"
B64_DIR = ROOT / "logo_batches" / "b64_slugs"


def js_for_group(slugs: list[str]) -> str:
    inner = ", ".join(json.dumps(s) for s in slugs)
    return (
        f"const slugs = [{inner}]; "
        "const out = {}; "
        'for (const s of slugs) { out[s] = figma.root.getSharedPluginData("ecosystem", "logo-" + s); } '
        "return out;"
    )


def main() -> None:
    groups = json.loads(GROUPS.read_text())
    have = {p.stem for p in B64_DIR.glob("*.txt")}
    missing_groups = []
    for i, slugs in enumerate(groups):
        if not all(s in have for s in slugs):
            missing_groups.append(i)
    print(f"b64 slugs: {len(have)}/146")
    print(f"missing groups: {len(missing_groups)}")
    if len(sys.argv) > 1 and sys.argv[1] == "codes":
        start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        for i in missing_groups[start : start + count]:
            print(f"GROUP {i}")
            print(js_for_group(groups[i]))
            print("---")


if __name__ == "__main__":
    main()
