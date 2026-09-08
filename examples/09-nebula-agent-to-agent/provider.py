from pathlib import Path

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent
HERE=Path(__file__).resolve().parent
agent=SecureAgent(config=config_path(HERE, "secureagent.conf"),nebula_config=config_path(HERE, "nebula.conf"))
agent.use_protocol("a2a",role="server",config=config_path(HERE, "provider-server.conf"))
@agent.skill("math.add")
def add(payload): return {"message": f"sum={int(payload.get('a',0))+int(payload.get('b',0))}"}
if __name__=="__main__": agent.run()
