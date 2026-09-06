.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . basic

run:
	cd $(ROOT) && uv run python examples/19-a2a-documentation-metadata/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
