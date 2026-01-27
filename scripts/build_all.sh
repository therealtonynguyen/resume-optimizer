#!/usr/bin/env bash
set -euo pipefail
./scripts/build_html.sh
./scripts/build_docx.sh
./scripts/build_pdf.sh
echo "All outputs are in ./build"
