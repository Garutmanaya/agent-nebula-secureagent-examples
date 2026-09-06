.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . oauth-nebula

run:
	cd $(ROOT) && uv run python examples/18-nebula-oauth-a2a/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
