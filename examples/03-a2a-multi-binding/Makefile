.PHONY: init run clean server client
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . basic

run:
	@target="$(word 2,$(MAKECMDGOALS))"; \
	case "$$target" in \
		server) cd $(ROOT) && uv run python $(CURDIR)/main.py ;; \
		client) cd $(ROOT) && uv run python $(CURDIR)/client.py ;; \
		*) echo "Usage: make run server | make run client" >&2; exit 2 ;; \
	esac

server client:
	@:

clean:
	rm -rf .data .runtime runtime certs secrets trust
