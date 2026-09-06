.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . nebula

run:
	cd $(ROOT) && uv run python examples/17-nebula-mtls/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
