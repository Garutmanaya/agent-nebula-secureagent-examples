"""A2A security example server."""
from pathlib import Path
from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent
HERE=Path(__file__).resolve().parent
agent=SecureAgent(config=config_path(HERE,"secureagent.conf"))
agent.use_protocol("a2a",role="server",config=config_path(HERE,"a2aserver.conf"))
@agent.skill("hello")
async def hello(payload):
    return {"message":"authenticated hello","payload":dict(payload)}
if __name__=="__main__": agent.run()
