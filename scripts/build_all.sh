#!/usr/bin/env bash
set -euo pipefail
# Convert resume.md to resume.dox first
python3 scripts/md_to_dox.py
./scripts/build_html.sh
./scripts/build_docx.sh
./scripts/build_pdf.sh
echo "All outputs are in ./build"
