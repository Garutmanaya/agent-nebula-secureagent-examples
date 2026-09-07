from pathlib import Path
from agent_nebula_secureagent import SecureAgent
HERE=Path(__file__).resolve().parent
agent=SecureAgent(config=HERE/"secureagent.conf",nebula_config=HERE/"nebula.conf")
agent.use_protocol("a2a",role="server",config=HERE/"orchestrator-server.conf")
agent.use_protocol("a2a",role="client",config=HERE/"a2aclient.conf")
@agent.skill("operations.add")
async def orchestrated_add(payload):
    providers=await agent.discover(capability="math.add")
    if not providers: return {"message":"no downstream math provider discovered"}
    responses=await agent.send_message(providers[0],data=payload,skill_id="math.add")
    message=responses[0].get("message",{})
    parts=message.get("parts",[]) if isinstance(message,dict) else []
    text=parts[0].get("text") if parts and isinstance(parts[0],dict) else None
    return {"message": text or "downstream response missing text"}
if __name__=="__main__": agent.run()
