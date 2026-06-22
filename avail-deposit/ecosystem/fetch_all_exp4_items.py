#!/usr/bin/env python3
"""Print MCP use_figma code snippets for all exp4 items (for batch fetching)."""

CHUNK_ITEMS = {i: 4 for i in range(36)}
CHUNK_ITEMS[36] = 2

for chunk, count in CHUNK_ITEMS.items():
    for idx in range(count):
        print(
            f"exp4-{chunk}-{idx}: "
            f"return JSON.parse(figma.root.getSharedPluginData('ecosystem', 'exp4-{chunk}'))[{idx}];"
        )
