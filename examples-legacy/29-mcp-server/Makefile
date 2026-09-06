.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . planned

run:
	cd $(ROOT) && uv run python examples/29-mcp-server/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
