#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/scripts/common.sh"

DIR="$(cd "$1" && pwd)"
resolve_example_paths "$DIR"

if [[ "$EXAMPLE_WORK_DIR" == "$DIR" ]]; then
  rm -rf "$DATA_DIR" "$RUNTIME_DIR" "$DIR/runtime" "$CERTS_DIR" "$SECRETS_DIR" "$TRUST_DIR"
else
  rm -rf "$EXAMPLE_WORK_DIR"
fi

log "Cleaned $(basename "$DIR")"
