.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . basic

run:
	cd $(ROOT) && uv run python examples/09-a2a-provider-metadata/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
