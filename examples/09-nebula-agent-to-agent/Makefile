.PHONY: init run clean provider orchestrator client
ROOT := ../..
init:
	$(ROOT)/scripts/init-example.sh . nebula-runtime
run:
	@target="$(word 2,$(MAKECMDGOALS))"; \
	case "$$target" in \
		provider) cd $(ROOT) && uv run python $(CURDIR)/provider.py ;; \
		orchestrator) cd $(ROOT) && uv run python $(CURDIR)/orchestrator.py ;; \
		client) cd $(ROOT) && uv run python $(CURDIR)/client.py ;; \
		*) echo "Usage: make run provider | make run orchestrator | make run client" >&2; exit 2 ;; \
	esac
provider orchestrator client:
	@:
clean:
	rm -rf .data .runtime runtime certs secrets trust
