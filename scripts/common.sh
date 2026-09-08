#!/usr/bin/env bash
set -euo pipefail

# Shared filesystem names. Keep the physical example layout in one place so
# initialization modes do not duplicate directory or filename conventions.
readonly EXAMPLE_RUNTIME_DIR_NAME=".runtime"
readonly EXAMPLE_DATA_DIR_NAME=".data"
readonly EXAMPLE_CONFIG_DIR_NAME="config"
readonly EXAMPLES_RUNTIME_ROOT_ENV="AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME"
readonly CERTS_DIR_NAME="certs"
readonly SECRETS_DIR_NAME="secrets"
readonly TRUST_DIR_NAME="trust"
readonly SERVER_KEY_FILENAME="server.key"
readonly SERVER_CERTIFICATE_FILENAME="server.crt"
readonly SERVER_CSR_FILENAME="server.csr"
readonly LOCAL_CA_KEY_FILENAME="local-ca.key"
readonly LOCAL_CA_CERTIFICATE_FILENAME="local-ca.crt"
readonly NEBULA_TRUST_BUNDLE_FILENAME="agent-nebula-ca.crt"
readonly ONBOARDING_API_KEY_FILENAME="onboarding-api-key"
readonly OAUTH_CLIENT_KEY_FILENAME="oauth-client.key"
readonly DEFAULT_CERTIFICATE_ORGANIZATION="Agent Nebula Examples"
readonly DEFAULT_CERTIFICATE_VALIDITY_DAYS="30"
readonly DEFAULT_RSA_KEY_BITS="3072"

log() { printf '[examples] %s\n' "$*"; }

require_command() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Required command not found: $1" >&2
    exit 1
  }
}

# Resolve the standard paths for one example. Callers use these variables
# instead of rebuilding .runtime/certs/secrets/trust paths themselves.
resolve_example_paths() {
  local dir="$1"
  local example_name
  example_name="$(basename "$dir")"

  EXAMPLE_DIR="$dir"
  if [[ -n "${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME:-}" ]]; then
    EXAMPLE_WORK_DIR="${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME%/}/$example_name"
    CONFIG_DIR="$EXAMPLE_WORK_DIR/$EXAMPLE_CONFIG_DIR_NAME"
  else
    EXAMPLE_WORK_DIR="$dir"
    CONFIG_DIR="$dir"
  fi

  DATA_DIR="$EXAMPLE_WORK_DIR/$EXAMPLE_DATA_DIR_NAME"
  RUNTIME_DIR="$EXAMPLE_WORK_DIR/$EXAMPLE_RUNTIME_DIR_NAME"
  CERTS_DIR="$EXAMPLE_WORK_DIR/$CERTS_DIR_NAME"
  SECRETS_DIR="$EXAMPLE_WORK_DIR/$SECRETS_DIR_NAME"
  TRUST_DIR="$EXAMPLE_WORK_DIR/$TRUST_DIR_NAME"
  RUNTIME_CERTS_DIR="$RUNTIME_DIR/$CERTS_DIR_NAME"
  RUNTIME_SECRETS_DIR="$RUNTIME_DIR/$SECRETS_DIR_NAME"
  RUNTIME_TRUST_DIR="$RUNTIME_DIR/$TRUST_DIR_NAME"

  SERVER_KEY_FILE="$RUNTIME_SECRETS_DIR/$SERVER_KEY_FILENAME"
  SERVER_CERTIFICATE_FILE="$RUNTIME_CERTS_DIR/$SERVER_CERTIFICATE_FILENAME"
  SERVER_CSR_FILE="$RUNTIME_CERTS_DIR/$SERVER_CSR_FILENAME"
  NEBULA_TRUST_BUNDLE_FILE="$RUNTIME_TRUST_DIR/$NEBULA_TRUST_BUNDLE_FILENAME"
  ONBOARDING_API_KEY_FILE="$RUNTIME_SECRETS_DIR/$ONBOARDING_API_KEY_FILENAME"
}

prepare_paths() {
  local dir="$1"
  resolve_example_paths "$dir"
  mkdir -p "$DATA_DIR" "$RUNTIME_DIR" "$CERTS_DIR" "$SECRETS_DIR" "$TRUST_DIR"
  chmod 700 "$SECRETS_DIR"
}

# When an external examples runtime root is configured, keep generated config
# beside that example's runtime/data. Source configuration remains immutable.
prepare_example_configs() {
  local dir="$1"
  resolve_example_paths "$dir"

  if [[ "$CONFIG_DIR" == "$dir" ]]; then
    return
  fi

  mkdir -p "$CONFIG_DIR"

  local source target
  for source in "$dir"/*.conf; do
    [[ -f "$source" ]] || continue
    target="$CONFIG_DIR/$(basename "$source")"
    cp "$source" "$target"

    # Runtime/application roots are authoritative absolute paths in generated
    # configuration. Explicit .runtime references are normalized as well.
    sed -i \
      -e "s|^product_root[[:space:]]*=.*$|product_root = $DATA_DIR|" \
      -e "s|^runtime_root[[:space:]]*=.*$|runtime_root = $RUNTIME_DIR|" \
      -e "s|\.runtime/|$RUNTIME_DIR/|g" \
      "$target"
  done

  log "Generated example configuration: $CONFIG_DIR"
}

prepare_runtime_tls_paths() {
  local dir="$1"
  resolve_example_paths "$dir"
  mkdir -p "$RUNTIME_CERTS_DIR" "$RUNTIME_SECRETS_DIR" "$RUNTIME_TRUST_DIR"
  chmod 700 "$RUNTIME_SECRETS_DIR"
}

# The host identity is configurable for CI/containers but defaults to the
# machine hostname. localhost and 127.0.0.1 remain SANs for local testing.
resolve_certificate_identity() {
  local example_name="$1"

  CERTIFICATE_HOSTNAME="${AGENT_NEBULA_EXAMPLE_HOSTNAME:-$(hostname)}"
  CERTIFICATE_ORGANIZATION="${AGENT_NEBULA_EXAMPLE_ORGANIZATION:-$DEFAULT_CERTIFICATE_ORGANIZATION}"
  CERTIFICATE_ORGANIZATIONAL_UNIT="${AGENT_NEBULA_EXAMPLE_NAME:-$example_name}"
  CERTIFICATE_SUBJECT="/CN=${CERTIFICATE_HOSTNAME}/O=${CERTIFICATE_ORGANIZATION}/OU=${CERTIFICATE_ORGANIZATIONAL_UNIT}"
  if [[ "$CERTIFICATE_HOSTNAME" == "localhost" ]]; then
    CERTIFICATE_SAN="DNS:localhost,IP:127.0.0.1"
  else
    CERTIFICATE_SAN="DNS:${CERTIFICATE_HOSTNAME},DNS:localhost,IP:127.0.0.1"
  fi
}

generate_private_key() {
  local key_file="$1"
  require_command openssl

  if [[ ! -f "$key_file" ]]; then
    openssl genpkey -algorithm RSA -pkeyopt "rsa_keygen_bits:${DEFAULT_RSA_KEY_BITS}" \
      -out "$key_file" >/dev/null 2>&1
    chmod 600 "$key_file"
  fi
}

generate_local_ca() {
  local dir="$1"
  require_command openssl
  prepare_paths "$dir"

  local ca_key_file="$SECRETS_DIR/$LOCAL_CA_KEY_FILENAME"
  local ca_certificate_file="$TRUST_DIR/$LOCAL_CA_CERTIFICATE_FILENAME"
  if [[ ! -f "$ca_certificate_file" ]]; then
    openssl req -x509 -newkey "rsa:${DEFAULT_RSA_KEY_BITS}" -sha256 \
      -days "$DEFAULT_CERTIFICATE_VALIDITY_DAYS" -nodes \
      -subj "/CN=Agent Nebula Examples Local CA" \
      -keyout "$ca_key_file" -out "$ca_certificate_file" >/dev/null 2>&1
    chmod 600 "$ca_key_file"
  fi
}

generate_server_certificate() {
  local dir="$1" name="$2"
  generate_local_ca "$dir"
  resolve_certificate_identity "$name"

  local server_key_file="$SECRETS_DIR/$SERVER_KEY_FILENAME"
  local server_certificate_file="$CERTS_DIR/$SERVER_CERTIFICATE_FILENAME"
  local csr_file="$RUNTIME_DIR/$SERVER_CSR_FILENAME"
  local extensions_file="$RUNTIME_DIR/server.ext"

  if [[ ! -f "$server_certificate_file" ]]; then
    generate_private_key "$server_key_file"
    openssl req -new -sha256 -key "$server_key_file" -subj "$CERTIFICATE_SUBJECT" \
      -addext "subjectAltName=${CERTIFICATE_SAN}" -out "$csr_file" >/dev/null 2>&1
    printf 'subjectAltName=%s\nextendedKeyUsage=serverAuth\n' "$CERTIFICATE_SAN" > "$extensions_file"
    openssl x509 -req -sha256 -days "$DEFAULT_CERTIFICATE_VALIDITY_DAYS" -in "$csr_file" \
      -CA "$TRUST_DIR/$LOCAL_CA_CERTIFICATE_FILENAME" \
      -CAkey "$SECRETS_DIR/$LOCAL_CA_KEY_FILENAME" -CAcreateserial \
      -extfile "$extensions_file" -out "$server_certificate_file" >/dev/null 2>&1
  fi
}

generate_runtime_local_ca() {
  local dir="$1"
  require_command openssl
  prepare_runtime_tls_paths "$dir"

  local ca_key_file="$RUNTIME_SECRETS_DIR/$LOCAL_CA_KEY_FILENAME"
  local ca_certificate_file="$RUNTIME_TRUST_DIR/$LOCAL_CA_CERTIFICATE_FILENAME"
  if [[ ! -f "$ca_certificate_file" ]]; then
    openssl req -x509 -newkey "rsa:${DEFAULT_RSA_KEY_BITS}" -sha256 \
      -days "$DEFAULT_CERTIFICATE_VALIDITY_DAYS" -nodes \
      -subj "/CN=Agent Nebula Examples Local CA" \
      -keyout "$ca_key_file" -out "$ca_certificate_file" >/dev/null 2>&1
    chmod 600 "$ca_key_file"
  fi
}

generate_runtime_server_certificate() {
  local dir="$1" name="$2"
  generate_runtime_local_ca "$dir"
  resolve_certificate_identity "$name"

  local extensions_file="$RUNTIME_DIR/server.ext"
  if [[ ! -f "$SERVER_CERTIFICATE_FILE" ]]; then
    generate_private_key "$SERVER_KEY_FILE"
    openssl req -new -sha256 -key "$SERVER_KEY_FILE" -subj "$CERTIFICATE_SUBJECT" \
      -addext "subjectAltName=${CERTIFICATE_SAN}" -out "$SERVER_CSR_FILE" >/dev/null 2>&1
    printf 'subjectAltName=%s\nextendedKeyUsage=serverAuth\n' "$CERTIFICATE_SAN" > "$extensions_file"
    openssl x509 -req -sha256 -days "$DEFAULT_CERTIFICATE_VALIDITY_DAYS" -in "$SERVER_CSR_FILE" \
      -CA "$RUNTIME_TRUST_DIR/$LOCAL_CA_CERTIFICATE_FILENAME" \
      -CAkey "$RUNTIME_SECRETS_DIR/$LOCAL_CA_KEY_FILENAME" -CAcreateserial \
      -extfile "$extensions_file" -out "$SERVER_CERTIFICATE_FILE" >/dev/null 2>&1
  fi
}

# Agent Nebula examples keep the private key on the agent host and submit only
# this CSR to Identity & Trust. Agent Nebula signs it and returns the public
# certificate; its trust bundle is installed separately during onboarding.
generate_runtime_server_csr() {
  local dir="$1" name="$2"
  prepare_runtime_tls_paths "$dir"
  resolve_certificate_identity "$name"
  generate_private_key "$SERVER_KEY_FILE"

  if [[ ! -f "$SERVER_CSR_FILE" ]]; then
    openssl req -new -sha256 \
      -key "$SERVER_KEY_FILE" \
      -subj "$CERTIFICATE_SUBJECT" \
      -addext "subjectAltName=${CERTIFICATE_SAN}" \
      -out "$SERVER_CSR_FILE" >/dev/null 2>&1
  fi

  log "Generated Agent Nebula CSR: $SERVER_CSR_FILE"
  log "CSR SANs: $CERTIFICATE_SAN"
  log "Private key remains local: $SERVER_KEY_FILE"
}

prepare_nebula_runtime_material_if_available() {
  local dir="$1"
  prepare_runtime_tls_paths "$dir"

  local source_trust_bundle="${AGENT_NEBULA_TRUST_BUNDLE_FILE:-}"
  if [[ -n "$source_trust_bundle" ]]; then
    [[ -f "$source_trust_bundle" ]] || {
      echo "AGENT_NEBULA_TRUST_BUNDLE_FILE does not exist: $source_trust_bundle" >&2
      exit 1
    }
    cp "$source_trust_bundle" "$NEBULA_TRUST_BUNDLE_FILE"
    log "Installed Agent Nebula trust bundle: $NEBULA_TRUST_BUNDLE_FILE"
  fi

  local api_key="${NEBULA_ONBOARDING_API_KEY:-}"
  if [[ -n "$api_key" ]]; then
    printf '%s' "$api_key" > "$ONBOARDING_API_KEY_FILE"
    chmod 600 "$ONBOARDING_API_KEY_FILE"
    log "Installed Agent Nebula onboarding API key: $ONBOARDING_API_KEY_FILE"
  fi
}

generate_client_key() {
  local dir="$1"
  require_command openssl
  prepare_paths "$dir"

  local key_file="$SECRETS_DIR/$OAUTH_CLIENT_KEY_FILENAME"
  if [[ ! -f "$key_file" ]]; then
    openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 \
      -out "$key_file" >/dev/null 2>&1
    chmod 600 "$key_file"
  fi
}

require_secret_from_env() {
  local dir="$1" env_name="$2" filename="$3"
  prepare_paths "$dir"

  local value="${!env_name:-}"
  local target_file="$SECRETS_DIR/$filename"
  if [[ -n "$value" ]]; then
    printf '%s' "$value" > "$target_file"
    chmod 600 "$target_file"
  elif [[ ! -s "$target_file" ]]; then
    log "$env_name is not set; $target_file must be provisioned before running this example."
  fi
}

prepare_nebula_runtime_material() {
  local dir="$1"
  prepare_runtime_tls_paths "$dir"

  local source_trust_bundle="${AGENT_NEBULA_TRUST_BUNDLE_FILE:-}"
  if [[ -n "$source_trust_bundle" ]]; then
    [[ -f "$source_trust_bundle" ]] || {
      echo "AGENT_NEBULA_TRUST_BUNDLE_FILE does not exist: $source_trust_bundle" >&2
      exit 1
    }
    cp "$source_trust_bundle" "$NEBULA_TRUST_BUNDLE_FILE"
  elif [[ ! -s "$NEBULA_TRUST_BUNDLE_FILE" ]]; then
    echo "Set AGENT_NEBULA_TRUST_BUNDLE_FILE or provision $NEBULA_TRUST_BUNDLE_FILE." >&2
    exit 1
  fi

  local api_key="${NEBULA_ONBOARDING_API_KEY:-}"
  if [[ -n "$api_key" ]]; then
    printf '%s' "$api_key" > "$ONBOARDING_API_KEY_FILE"
    chmod 600 "$ONBOARDING_API_KEY_FILE"
  elif [[ ! -s "$ONBOARDING_API_KEY_FILE" ]]; then
    echo "Set NEBULA_ONBOARDING_API_KEY or provision $ONBOARDING_API_KEY_FILE." >&2
    exit 1
  fi
}

prepare_runtime_oauth_keys() {
  local dir="$1"
  require_command openssl
  prepare_runtime_tls_paths "$dir"

  local name key_file
  for name in oauth-auth dpop; do
    key_file="$RUNTIME_SECRETS_DIR/$name.key"
    if [[ ! -f "$key_file" ]]; then
      openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 \
        -out "$key_file" >/dev/null 2>&1
      chmod 600 "$key_file"
    fi
  done
}
