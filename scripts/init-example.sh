#!/usr/bin/env bash
set -euo pipefail

# Central entry point for example initialization. Example Makefiles select an
# initialization mode; all filesystem and cryptographic conventions live in
# common.sh so individual examples do not duplicate provisioning logic.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/scripts/common.sh"

DIR="$(cd "$1" && pwd)"
MODE="${2:-basic}"
EXAMPLE_NAME="$(basename "$DIR")"

prepare_paths "$DIR"
prepare_example_configs "$DIR"

case "$MODE" in
  basic)
    # No TLS or Agent Nebula credentials are required.
    ;;
  tls)
    # Local CA and TLS material in the legacy top-level example directories.
    generate_server_certificate "$DIR" "$EXAMPLE_NAME"
    ;;
  tls-runtime)
    # Local CA and TLS material inside the managed .runtime boundary.
    generate_runtime_server_certificate "$DIR" "$EXAMPLE_NAME"
    ;;
  oauth)
    generate_server_certificate "$DIR" "$EXAMPLE_NAME"
    generate_client_key "$DIR"
    ;;
  nebula)
    generate_server_certificate "$DIR" "$EXAMPLE_NAME"
    require_secret_from_env "$DIR" NEBULA_ONBOARDING_API_KEY "$ONBOARDING_API_KEY_FILENAME"
    ;;
  oauth-nebula)
    generate_server_certificate "$DIR" "$EXAMPLE_NAME"
    generate_client_key "$DIR"
    require_secret_from_env "$DIR" NEBULA_ONBOARDING_API_KEY "$ONBOARDING_API_KEY_FILENAME"
    ;;
  nebula-csr)
    # Real Agent Nebula onboarding: generate identity locally, then submit only
    # the public CSR to Identity & Trust for certificate issuance.
    generate_runtime_server_csr "$DIR" "$EXAMPLE_NAME"
    prepare_nebula_runtime_material_if_available "$DIR"
    log "Next: submit $SERVER_CSR_FILE in Agent Nebula Provider > Certificates."
    log "Then install server.crt, $NEBULA_TRUST_BUNDLE_FILENAME, and the onboarding API key under $RUNTIME_DIR."
    ;;
  nebula-runtime)
    generate_runtime_server_certificate "$DIR" "$EXAMPLE_NAME"
    prepare_nebula_runtime_material "$DIR"
    ;;
  oauth-nebula-runtime)
    generate_runtime_server_certificate "$DIR" "$EXAMPLE_NAME"
    prepare_nebula_runtime_material "$DIR"
    prepare_runtime_oauth_keys "$DIR"
    ;;
  planned)
    log "Prepared paths only. This example requires a Platform protocol adapter that is not available yet."
    ;;
  *)
    echo "Unknown initialization mode: $MODE" >&2
    exit 2
    ;;
esac

log "Initialized $EXAMPLE_NAME"
