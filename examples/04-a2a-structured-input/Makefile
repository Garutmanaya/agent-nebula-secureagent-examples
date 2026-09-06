.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . basic

run:
	cd $(ROOT) && uv run python examples/04-a2a-structured-input/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
