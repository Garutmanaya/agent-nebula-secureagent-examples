.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . tls

run:
	cd $(ROOT) && uv run python examples/08-a2a-tls/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
