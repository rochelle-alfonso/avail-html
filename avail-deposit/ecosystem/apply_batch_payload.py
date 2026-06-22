#!/usr/bin/env python3
"""Save {id, data} batch payload to logo_batches and export PNGs."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    path = Path(sys.argv[1])
    payload = json.loads(path.read_text())
    proc = subprocess.run(
        [sys.executable, str(ROOT / "save_batches_stdin.py")],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
    )
    print(proc.stdout.strip() or proc.stderr.strip())
    batch_id = str(payload["id"])
    proc2 = subprocess.run(
        [sys.executable, str(ROOT / "export_partner_logos.py"), batch_id],
        capture_output=True,
        text=True,
    )
    print(proc2.stdout.strip() or proc2.stderr.strip())
    n = len(list((ROOT / "assets/partners").glob("*.png")))
    print(f"PNG count: {n}")


if __name__ == "__main__":
    main()
