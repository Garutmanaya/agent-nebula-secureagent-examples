.PHONY: init run clean
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . basic

run:
	cd $(ROOT) && uv run python examples/05-a2a-structured-result/main.py

clean:
	rm -rf .runtime runtime certs secrets trust
