#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
find "$ROOT/examples" -mindepth 2 -maxdepth 2 \( -name .runtime -o -name runtime -o -name certs -o -name secrets -o -name trust \) -type d -prune -exec rm -rf {} +
