"""Structured result."""
from agent_nebula_secureagent import SecureAgent

agent = SecureAgent()
agent.use_protocol("a2a", role="server", config="a2aserver.conf")

@agent.skill("example.invoke")
def handle(payload):
    """Execute the example business capability."""
    return {"status": "ok", "items": [{"id": "A-100", "quantity": 12}]}

if __name__ == "__main__":
    agent.run()
