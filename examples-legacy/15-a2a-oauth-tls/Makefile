.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . oauth

run:
	cd $(ROOT) && uv run python examples/15-a2a-oauth-tls/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
