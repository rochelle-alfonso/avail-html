#!/usr/bin/env python3
"""Save one inbox JSON file (slug->b64 map) and apply via apply_b64_json.py."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INBOX = ROOT / "logo_batches" / "inbox"


def main() -> None:
    INBOX.mkdir(parents=True, exist_ok=True)
    if len(sys.argv) > 1:
        src = Path(sys.argv[1])
        data = json.loads(src.read_text())
    else:
        data = json.load(sys.stdin)
    proc = subprocess.run(
        [sys.executable, str(ROOT / "apply_b64_json.py")],
        input=json.dumps(data),
        text=True,
        capture_output=True,
    )
    print(proc.stdout.strip() or proc.stderr.strip())
    print(f"PNG count: {len(list((ROOT / 'assets' / 'partners').glob('*.png')))}")


if __name__ == "__main__":
    main()
