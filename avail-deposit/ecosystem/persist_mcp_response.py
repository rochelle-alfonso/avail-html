#!/usr/bin/env python3
"""Persist MCP use_figma JSON response to logo_batches/exp4-{id}.json or parts."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
PARTS = BATCHES / "parts"


def strip_truncation(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s*//\s*truncated to 20kb\s*$", "", text, flags=re.IGNORECASE)
    return text


def parse_payload(text: str):
    text = strip_truncation(text)
    if text.startswith("["):
        return json.loads(text)
    if text.startswith("{"):
        return json.loads(text)
    start = text.find("[")
    if start != -1:
        end = text.rfind("]")
        if end > start:
            return json.loads(text[start : end + 1])
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return json.loads(text[start : end + 1])
    raise ValueError("No JSON found")


def b64_ok(b64: str) -> bool:
    return len(b64) > 100 and b64.endswith(("QmCC", "QkCC", "ggg==", "AAA=", "CYII="))


def save_chunk(chunk_id: int, data: list) -> None:
    dest = BATCHES / f"exp4-{chunk_id}.json"
    dest.write_text(json.dumps(data))
    print(f"Saved {dest.name} ({len(data)} items)")
    for item in data:
        b64 = item.get("b64") or ""
        status = "OK" if b64_ok(b64) else f"BAD len={len(b64)} ends={b64[-12:] if b64 else 'none'}"
        print(f"  {item['name']}: {status}")


def save_part(chunk_id: int, index: int, item: dict) -> None:
    PARTS.mkdir(parents=True, exist_ok=True)
    dest = PARTS / f"exp4-{chunk_id}-{index}.json"
    dest.write_text(json.dumps(item))
    b64 = item.get("b64") or ""
    print(f"Saved {dest.name} ({item['name']}) b64={len(b64)}")


def main() -> None:
    mode = sys.argv[1]  # chunk | part
    raw = Path(sys.argv[-1]).read_text() if Path(sys.argv[-1]).exists() else sys.stdin.read()
    data = parse_payload(raw)
    if mode == "chunk":
        chunk_id = int(sys.argv[2])
        if not isinstance(data, list):
            raise SystemExit("Expected JSON array for chunk mode")
        save_chunk(chunk_id, data)
    elif mode == "part":
        chunk_id, index = int(sys.argv[2]), int(sys.argv[3])
        if isinstance(data, list):
            data = data[0]
        save_part(chunk_id, index, data)
    else:
        raise SystemExit(f"Unknown mode: {mode}")


if __name__ == "__main__":
    main()
