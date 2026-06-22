#!/bin/bash
# After slice JSON files exist in logo_batches/slices/, merge and save all chunks.
set -euo pipefail
cd "$(dirname "$0")"
python3 merge_slices.py
ls assets/partners | wc -l
