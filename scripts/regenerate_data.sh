#!/usr/bin/env bash
# ============================================================
# regenerate_data.sh
# Regenerates all election JS data files:
#   data/election66_data.js
#   data/election69_ocr.js
#   data/election69_94pct.js
#
# Usage: bash scripts/regenerate_data.sh
#        (Run from the project root)
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║   Thailand Election Data Regeneration Script     ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ── Step 1: Build election66_data.js and election69_ocr.js ──
echo "▶ Step 1/3: Building election66_data.js + election69_ocr.js..."
cd "$SCRIPT_DIR"
python build_election_data.py
echo "✓ Done."
echo ""

# ── Step 2: Build election69_94pct.js from Excel ────────────
echo "▶ Step 2/3: Extracting 94% unofficial data → data/election69_94pct.js..."
python extract_94pct_data.py
echo "✓ Done."
echo ""

# ── Step 3: Run split_data.py to finalise all split files ───
echo "▶ Step 3/3: Running split_data.py to generate final split files..."
python split_data.py
echo "✓ Done."
echo ""

# ── Summary ──────────────────────────────────────────────────
echo "════════════════════════════════════════════════"
echo "All data files regenerated successfully!"
echo ""
echo "Updated files:"
echo "  • $ROOT_DIR/data/election66_data.js"
echo "  • $ROOT_DIR/data/election69_ocr.js"
echo "  • $ROOT_DIR/data/election69_94pct.js"
echo ""
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S %Z")
echo "  Timestamp: $TIMESTAMP"
echo "════════════════════════════════════════════════"
echo ""
echo "To preview: python -m http.server (from project root)"
echo ""
