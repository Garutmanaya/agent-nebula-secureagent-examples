.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . basic

run:
	cd $(ROOT) && uv run python examples/11-a2a-capabilities/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
