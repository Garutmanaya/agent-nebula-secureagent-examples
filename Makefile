# Local environment URLs. Shell values override values loaded from .env.
-include .env
export

.PHONY: install lint list env-init pki-init nebula-pki-init secrets-init a2ui-init a2ui-web-build init run clean nebula-proxy-config help server client browser provider orchestrator

EXAMPLE := $(word 2,$(MAKECMDGOALS))
PROCESS := $(word 3,$(MAKECMDGOALS))

install:
	uv sync --group dev

lint:
	uv run ruff check examples examples-nebula

help:
	@echo "Agent Nebula SecureAgent examples"
	@echo "  make env-init"
	@echo "  make pki-init              # local development PKI"
	@echo "  make nebula-pki-init       # Agent Nebula enrollment keys + CSRs"
	@echo "  make secrets-init"
	@echo "  make a2ui-init            # install shared A2UI browser packages"
	@echo "  make a2ui-web-build       # build shared A2UI browser renderer"
	@echo "  make list"
	@echo "  make init example-01"
	@echo "  make run example-01 server"
	@echo "  make run example-01 client"
	@echo "  make clean example-01"
	@echo "  make init all"
	@echo "  make clean all"

list:
	@./scripts/example-lifecycle.py list

env-init:
	@./scripts/example-lifecycle.py env-init

pki-init:
	@./scripts/example-lifecycle.py pki-init

nebula-pki-init:
	@./scripts/example-lifecycle.py nebula-pki-init

secrets-init:
	@./scripts/example-lifecycle.py secrets-init

a2ui-init:
	@./scripts/a2ui-web-init.sh

a2ui-web-build: a2ui-init
	@npm --prefix examples/common/a2ui-web run build

init:
	@if [ -z "$(EXAMPLE)" ]; then echo "Usage: make init example-NN | make init all" >&2; exit 2; fi
	@./scripts/example-lifecycle.py init "$(EXAMPLE)"

run:
	@if [ -z "$(EXAMPLE)" ] || [ -z "$(PROCESS)" ]; then echo "Usage: make run example-NN <process>" >&2; exit 2; fi
	@./scripts/example-lifecycle.py run "$(EXAMPLE)" "$(PROCESS)"

clean:
	@if [ -z "$(EXAMPLE)" ]; then echo "Usage: make clean example-NN | make clean all" >&2; exit 2; fi
	@./scripts/example-lifecycle.py clean "$(EXAMPLE)"

# Selector goals consumed by init/run/clean.
example-%:
	@:

all server client browser provider orchestrator:
	@:

# Generate local Nginx routing for the hosted Agent Nebula integration examples.
# NGROK_DOMAIN and the upstream TLS CA bundle must be explicitly configured.
nebula-proxy-config:
	@test -n "$(NGROK_DOMAIN)" || (echo "Set NGROK_DOMAIN to your assigned ngrok hostname" >&2; exit 2)
	@python3 scripts/nebula-public-endpoint.py --domain "$(NGROK_DOMAIN)" --ca-file "$(NEBULA_PROXY_CA_FILE)" --upstream-tls-name "$(or $(NEBULA_PROXY_TLS_NAME),localhost)" --output "$(or $(NEBULA_PROXY_OUTPUT),$(AGENT_NEBULA_EXAMPLES_ROOT)/proxy)"
