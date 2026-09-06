.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . basic

run:
	cd $(ROOT) && uv run python examples/02-a2a-async-skill/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
