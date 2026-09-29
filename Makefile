.PHONY: install lint list env-init init run clean help server client provider orchestrator

EXAMPLE := $(word 2,$(MAKECMDGOALS))
PROCESS := $(word 3,$(MAKECMDGOALS))

install:
	uv sync --group dev

lint:
	uv run ruff check examples

help:
	@echo "Agent Nebula SecureAgent examples"
	@echo "  make env-init"
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

all server client provider orchestrator:
	@:
