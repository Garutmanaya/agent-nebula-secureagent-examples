"""A2UI surface: forward-compatible SecureAgent API example.

This source intentionally uses only the protocol-neutral public API. The selected
adapter is not available in the current Platform/SecureAgent release; see README.md.
"""
from agent_nebula_secureagent import SecureAgent

agent = SecureAgent()
agent.use_protocol("a2a", role="server", config="a2aserver.conf")

@agent.skill("example.invoke")
def example(payload):
    return {"received": dict(payload)}

if __name__ == "__main__":
    agent.run()
