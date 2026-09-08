#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for makefile in "$ROOT"/examples/*/Makefile; do
  make -s -C "$(dirname "$makefile")" clean
done
