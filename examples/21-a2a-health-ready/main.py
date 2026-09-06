"""Platform health."""
from agent_nebula_secureagent import SecureAgent

agent = SecureAgent()
agent.use_protocol("a2a", role="server", config="a2aserver.conf")

@agent.skill("example.invoke")
def handle(payload):
    """Execute the example business capability."""
    return {"message": "hello from SecureAgent", "payload": dict(payload)}

if __name__ == "__main__":
    agent.run()
