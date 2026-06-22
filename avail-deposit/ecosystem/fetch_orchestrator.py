#!/usr/bin/env python3
"""Orchestrate fetching missing partner logos via use_figma MCP slices.

Prints MCP JavaScript for missing 2-partner slices, or applies existing slice files.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
META = ROOT / "logo_batches" / "meta"
B64 = ROOT / "logo_batches" / "b64"
SLICES = ROOT / "logo_batches" / "slices"


def chunk_sizes() -> list[int]:
    return [len(json.loads((META / f"export-{c}.json").read_text())) for c in range(19)]


def missing_slices() -> list[tuple[int, int]]:
    missing = []
    for chunk, n in enumerate(chunk_sizes()):
        for start in range(0, n, 2):
            end = min(start + 2, n)
            for i in range(start, end):
                if not (B64 / f"export-{chunk}-{i}.txt").exists():
                    missing.append((chunk, start))
                    break
    return missing


def mcp_code(chunk: int, start: int) -> str:
    return (
        f"const d = JSON.parse(figma.root.getSharedPluginData('ecosystem', 'export-{chunk}')); "
        f"return d.slice({start}, {start + 2}).map(p => p.b64);"
    )


def apply_slices() -> int:
    applied = 0
    for chunk, n in enumerate(chunk_sizes()):
        for start in range(0, n, 2):
            src = SLICES / f"export-{chunk}-{start}.json"
            if src.exists():
                subprocess.run(
                    [sys.executable, str(ROOT / "save_b64_array_stdin.py"), str(chunk), str(start)],
                    input=src.read_text(),
                    text=True,
                    check=True,
                )
                applied += 1
    return applied


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        sizes = chunk_sizes()
        total = sum(sizes)
        have = len(list(B64.glob("export-*-*.txt")))
        print(f"b64 files: {have}/{total}")
        for chunk, start in missing_slices()[:20]:
            print(f"  missing slice export-{chunk}-{start}")
        if len(missing_slices()) > 20:
            print(f"  ... {len(missing_slices())} slices total")
    elif cmd == "codes":
        for chunk, start in missing_slices():
            print(f"CHUNK={chunk} START={start}")
            print(mcp_code(chunk, start))
            print("---")
    elif cmd == "assemble":
        subprocess.run([sys.executable, str(ROOT / "assemble_from_b64.py")], check=True)
        count = len(list((ROOT / "assets" / "partners").glob("*.png")))
        print(f"PNG count: {count}")
    elif cmd == "apply":
        n = apply_slices()
        print(f"Applied {n} slices")
        subprocess.run([sys.executable, str(ROOT / "assemble_from_b64.py")], check=True)


if __name__ == "__main__":
    main()
