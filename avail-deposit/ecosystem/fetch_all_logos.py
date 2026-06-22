#!/usr/bin/env python3
"""Fetch all partner logo batches from Figma via use_figma MCP and save PNGs.

Run from ecosystem/ after batches are stored in Figma shared plugin data.
This script reads batch JSON files from logo_batches/ if present,
otherwise prints instructions.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
OUT = ROOT / "assets" / "partners"


def main() -> None:
    if not BATCHES.exists() or not any(BATCHES.glob("batch-*.json")):
        print("No logo_batches/*.json found. Export batches from Figma first.")
        sys.exit(1)
    subprocess.run([sys.executable, str(ROOT / "export_partner_logos.py")], check=True)
    count = len(list(OUT.glob("*.png")))
    print(f"Partner logos ready: {count}")


if __name__ == "__main__":
    main()
