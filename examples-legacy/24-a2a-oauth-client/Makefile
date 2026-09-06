.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . planned

run:
	cd $(ROOT) && uv run python examples/24-a2a-oauth-client/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
