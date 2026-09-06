.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . basic

run:
	cd $(ROOT) && uv run python examples/03-a2a-custom-scope/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
