.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . basic

run:
	cd $(ROOT) && uv run python examples/10-a2a-content-modes/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
