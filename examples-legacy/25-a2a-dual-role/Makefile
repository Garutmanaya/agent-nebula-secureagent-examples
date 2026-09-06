.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . planned

run:
	cd $(ROOT) && uv run python examples/25-a2a-dual-role/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
