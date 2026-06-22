#!/usr/bin/env python3
"""Save a chunk JSON array from a file argument (raw MCP response text)."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
BATCHES.mkdir(exist_ok=True)


def extract_json_array(text: str) -> list:
    text = text.strip()
    if text.startswith("["):
        # Strip MCP truncation suffix if appended outside JSON
        m = re.search(r"\]\s*(?://[^\[]*$)", text, re.DOTALL)
        if m:
            text = text[: m.end()].rstrip()
            if not text.endswith("]"):
                text = text[: text.rindex("]") + 1]
        return json.loads(text)
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("No JSON array found in input")
    return json.loads(text[start : end + 1])


def main() -> None:
    chunk_id = sys.argv[1]
    raw = Path(sys.argv[2]).read_text() if len(sys.argv) > 2 else sys.stdin.read()
    data = extract_json_array(raw)
    out = BATCHES / f"exp4-{chunk_id}.json"
    out.write_text(json.dumps(data))
    print(f"Saved {out.name} ({len(data)} items)")
    for item in data:
        b64 = item.get("b64", "")
        ok = len(b64) > 100 and b64.endswith(("QmCC", "QkCC", "ggg==", "AAA="))
        print(f"  {item['name']}: b64 len={len(b64)} {'OK' if ok else 'TRUNCATED?'}")


if __name__ == "__main__":
    main()
