.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . basic

run:
	cd $(ROOT) && uv run python examples/06-a2a-application-paths/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
