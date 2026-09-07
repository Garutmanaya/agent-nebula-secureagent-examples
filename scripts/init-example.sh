#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/scripts/common.sh"
DIR="$(cd "$1" && pwd)"
MODE="${2:-basic}"
prepare_paths "$DIR"
case "$MODE" in
  basic) ;;
  tls) generate_server_certificate "$DIR" "$(basename "$DIR")" ;;
  tls-runtime) generate_runtime_server_certificate "$DIR" "$(basename "$DIR")" ;;
  oauth) generate_server_certificate "$DIR" "$(basename "$DIR")"; generate_client_key "$DIR" ;;
  nebula) generate_server_certificate "$DIR" "$(basename "$DIR")"; require_secret_from_env "$DIR" NEBULA_ONBOARDING_API_KEY onboarding-api-key ;;
  oauth-nebula) generate_server_certificate "$DIR" "$(basename "$DIR")"; generate_client_key "$DIR"; require_secret_from_env "$DIR" NEBULA_ONBOARDING_API_KEY onboarding-api-key ;;
  nebula-runtime) generate_runtime_server_certificate "$DIR" "$(basename "$DIR")"; prepare_nebula_runtime_material "$DIR" ;;
  oauth-nebula-runtime) generate_runtime_server_certificate "$DIR" "$(basename "$DIR")"; prepare_nebula_runtime_material "$DIR"; prepare_runtime_oauth_keys "$DIR" ;;
  planned) log "Prepared paths only. This example requires a Platform protocol adapter that is not available yet." ;;
  *) echo "Unknown initialization mode: $MODE" >&2; exit 2 ;;
esac
log "Initialized $(basename "$DIR")"
