#!/usr/bin/env python3
"""Fetch all exp4 chunks from Figma shared plugin data via use_figma MCP.

Usage: run from ecosystem/ — requires manual MCP calls or pre-saved chunk JSON files.
This script processes saved exp4-*.json files and writes PNGs.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "fetch_exp4_chunks.py")], check=True)


if __name__ == "__main__":
    main()
