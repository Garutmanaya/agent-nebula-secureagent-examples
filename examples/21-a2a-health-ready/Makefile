.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . basic

run:
	cd $(ROOT) && uv run python examples/21-a2a-health-ready/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
