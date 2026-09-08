.PHONY: init run clean server client
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . tls-runtime

run:
	@target="$(word 2,$(MAKECMDGOALS))"; \
	case "$$target" in \
		server) cd $(ROOT) && PYTHONPATH="$(abspath $(ROOT))$${PYTHONPATH:+:$${PYTHONPATH}}" AGENT_NEBULA_EXAMPLE_CONFIG_DIR="$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME:+$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME%/}/$(notdir $(CURDIR))/config}" uv run python $(CURDIR)/main.py ;; \
		client) cd $(ROOT) && PYTHONPATH="$(abspath $(ROOT))$${PYTHONPATH:+:$${PYTHONPATH}}" AGENT_NEBULA_EXAMPLE_CONFIG_DIR="$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME:+$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME%/}/$(notdir $(CURDIR))/config}" uv run python $(CURDIR)/client.py ;; \
		*) echo "Usage: make run server | make run client" >&2; exit 2 ;; \
	esac

server client:
	@:

clean:
	$(ROOT)/scripts/clean-example.sh .
