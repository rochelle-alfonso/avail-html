# exp4 Partner Logo Fetch (per-item)

Full chunks truncate at ~20KB in MCP responses. Fetch **one logo per `use_figma` call**.

## use_figma code (chunk `C`, item index `I`)

```javascript
const raw = figma.root.getSharedPluginData('ecosystem', 'exp4-C');
const items = JSON.parse(raw);
return items[I];
```

Replace `C` and `I` (0–3). Always pass `skillNames: "figma-use"`, `fileKey: gNLzTEOcVqalc9OkJJkCqO`.

## Save each item

```bash
python3 save_exp4_part_stdin.py C I <<'EOF'
<paste JSON object from use_figma>
EOF
```

## After all 148 items (37×4)

```bash
python3 assemble_exp4_parts.py
python3 fetch_exp4_chunks.py
```

## Status

```bash
python3 -c "
from pathlib import Path
parts = Path('logo_batches/parts')
for c in range(37):
    n = len(list(parts.glob(f'exp4-{c}-*.json')))
    print(f'chunk {c}: {n}/4')
"
```
