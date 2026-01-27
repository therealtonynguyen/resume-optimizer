#!/usr/bin/env bash
set -euo pipefail
mkdir -p build/doxygen
doxygen Doxyfile
echo "HTML generated at build/doxygen/html/index.html"
