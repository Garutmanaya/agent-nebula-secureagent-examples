#!/usr/bin/env bash
set -euo pipefail

log() { printf '[examples] %s\n' "$*"; }
require_command() { command -v "$1" >/dev/null 2>&1 || { echo "Required command not found: $1" >&2; exit 1; }; }
prepare_paths() {
  local dir="$1"
  mkdir -p "$dir/.runtime" "$dir/certs" "$dir/secrets" "$dir/trust"
  chmod 700 "$dir/secrets"
}
generate_local_ca() {
  local dir="$1"
  require_command openssl
  if [[ ! -f "$dir/trust/local-ca.crt" ]]; then
    openssl req -x509 -newkey rsa:3072 -sha256 -days 30 -nodes \
      -subj "/CN=Agent Nebula Examples Local CA" \
      -keyout "$dir/secrets/local-ca.key" -out "$dir/trust/local-ca.crt" >/dev/null 2>&1
    chmod 600 "$dir/secrets/local-ca.key"
  fi
}
generate_server_certificate() {
  local dir="$1" name="$2"
  generate_local_ca "$dir"
  if [[ ! -f "$dir/certs/server.crt" ]]; then
    openssl req -new -newkey rsa:3072 -nodes -subj "/CN=localhost" \
      -keyout "$dir/secrets/server.key" -out "$dir/.runtime/server.csr" >/dev/null 2>&1
    printf 'subjectAltName=DNS:localhost,IP:127.0.0.1\nextendedKeyUsage=serverAuth\n' > "$dir/.runtime/server.ext"
    openssl x509 -req -sha256 -days 30 -in "$dir/.runtime/server.csr" \
      -CA "$dir/trust/local-ca.crt" -CAkey "$dir/secrets/local-ca.key" -CAcreateserial \
      -extfile "$dir/.runtime/server.ext" -out "$dir/certs/server.crt" >/dev/null 2>&1
    chmod 600 "$dir/secrets/server.key"
  fi
}
generate_client_key() {
  local dir="$1"
  require_command openssl
  if [[ ! -f "$dir/secrets/oauth-client.key" ]]; then
    openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 \
      -out "$dir/secrets/oauth-client.key" >/dev/null 2>&1
    chmod 600 "$dir/secrets/oauth-client.key"
  fi
}
require_secret_from_env() {
  local dir="$1" env_name="$2" filename="$3"
  local value="${!env_name:-}"
  if [[ -n "$value" ]]; then
    printf '%s' "$value" > "$dir/secrets/$filename"
    chmod 600 "$dir/secrets/$filename"
  elif [[ ! -s "$dir/secrets/$filename" ]]; then
    log "$env_name is not set; $dir/secrets/$filename must be provisioned before running this example."
  fi
}
