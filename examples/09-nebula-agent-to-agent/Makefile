.PHONY: init run clean provider orchestrator client
ROOT := ../..
init:
	$(ROOT)/scripts/init-example.sh . nebula-runtime
run:
	@target="$(word 2,$(MAKECMDGOALS))"; \
	case "$$target" in \
		provider) cd $(ROOT) && PYTHONPATH="$(abspath $(ROOT))$${PYTHONPATH:+:$${PYTHONPATH}}" AGENT_NEBULA_EXAMPLE_CONFIG_DIR="$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME:+$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME%/}/$(notdir $(CURDIR))/config}" uv run python $(CURDIR)/provider.py ;; \
		orchestrator) cd $(ROOT) && PYTHONPATH="$(abspath $(ROOT))$${PYTHONPATH:+:$${PYTHONPATH}}" AGENT_NEBULA_EXAMPLE_CONFIG_DIR="$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME:+$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME%/}/$(notdir $(CURDIR))/config}" uv run python $(CURDIR)/orchestrator.py ;; \
		client) cd $(ROOT) && PYTHONPATH="$(abspath $(ROOT))$${PYTHONPATH:+:$${PYTHONPATH}}" AGENT_NEBULA_EXAMPLE_CONFIG_DIR="$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME:+$${AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME%/}/$(notdir $(CURDIR))/config}" uv run python $(CURDIR)/client.py ;; \
		*) echo "Usage: make run provider | make run orchestrator | make run client" >&2; exit 2 ;; \
	esac
provider orchestrator client:
	@:
clean:
	$(ROOT)/scripts/clean-example.sh .
