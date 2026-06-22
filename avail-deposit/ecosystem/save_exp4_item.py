#!/usr/bin/env python3
"""Save single exp4 logo item and assemble complete chunk files."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
ITEMS = BATCHES / "items"
BATCHES.mkdir(exist_ok=True)
ITEMS.mkdir(exist_ok=True)


def save_item(chunk_id: int, item_idx: int, item: dict) -> None:
    path = ITEMS / f"exp4-{chunk_id}-{item_idx}.json"
    path.write_text(json.dumps(item))
    print(f"Saved {path.name}: {item['name']}")


def assemble_chunk(chunk_id: int) -> bool:
    items = []
    for i in range(4):
        path = ITEMS / f"exp4-{chunk_id}-{i}.json"
        if not path.exists():
            return False
        items.append(json.loads(path.read_text()))
    out = BATCHES / f"exp4-{chunk_id}.json"
    out.write_text(json.dumps(items))
    print(f"Assembled {out.name} ({len(items)} items)")
    return True


def assemble_all() -> int:
    done = 0
    for chunk_id in range(37):
        if assemble_chunk(chunk_id):
            done += 1
    return done


def status() -> dict:
    chunks_complete = 0
    items_saved = 0
    missing = []
    for chunk_id in range(37):
        have = sum(1 for i in range(4) if (ITEMS / f"exp4-{chunk_id}-{i}.json").exists())
        items_saved += have
        if have == 4:
            chunks_complete += 1
        else:
            for i in range(4):
                if not (ITEMS / f"exp4-{chunk_id}-{i}.json").exists():
                    missing.append(f"exp4-{chunk_id}-{i}")
    return {
        "chunks_complete": chunks_complete,
        "items_saved": items_saved,
        "missing": missing,
    }


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps(status(), indent=2))
        return
    cmd = sys.argv[1]
    if cmd == "save" and len(sys.argv) >= 4:
        chunk_id = int(sys.argv[2])
        item_idx = int(sys.argv[3])
        item = json.load(sys.stdin)
        save_item(chunk_id, item_idx, item)
        assemble_chunk(chunk_id)
    elif cmd == "assemble":
        print(f"Assembled {assemble_all()} chunks")
    elif cmd == "status":
        print(json.dumps(status(), indent=2))
    else:
        print("Usage: save_exp4_item.py save <chunk> <idx> | assemble | status", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
