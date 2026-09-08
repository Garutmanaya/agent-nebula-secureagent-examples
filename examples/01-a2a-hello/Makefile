.PHONY: init run clean server client
ROOT := ../..

init:
	$(ROOT)/scripts/init-example.sh . basic

run:
	@target="$(word 2,$(MAKECMDGOALS))"; \
	case "$$target" in \
		server) cd $(ROOT) && PYTHONPATH="$(abspath $(ROOT))$${PYTHONPATH:+:$${PYTHONPATH}}" AGENT_NEBULA_EXAMPLE_CONFIG_DIR="$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME:+$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME%/}/$(notdir $(CURDIR))/config}" uv run python examples/01-a2a-hello/main.py ;; \
		client) cd $(ROOT) && PYTHONPATH="$(abspath $(ROOT))$${PYTHONPATH:+:$${PYTHONPATH}}" AGENT_NEBULA_EXAMPLE_CONFIG_DIR="$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME:+$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME%/}/$(notdir $(CURDIR))/config}" uv run python examples/01-a2a-hello/client.py ;; \
		*) echo "Usage: make run server | make run client" >&2; exit 2 ;; \
	esac

# `server` and `client` are selector goals consumed by `run`.
server client:
	@:

clean:
	$(ROOT)/scripts/clean-example.sh .
