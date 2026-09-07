import asyncio
from pathlib import Path
from agent_nebula_secureagent import SecureAgent
HERE=Path(__file__).resolve().parent
async def main():
    agent=SecureAgent(config=HERE/"secureagent.conf",nebula_config=HERE/"nebula.conf")
    agent.use_protocol("a2a",role="client",config=HERE/"a2aclient.conf")
    try:
        agents=await agent.discover(capability="operations.add")
        if not agents: raise AssertionError("orchestrator not discovered")
        response=await agent.send_message(agents[0],data={"a":20,"b":22},skill_id="operations.add")
        text=response[0]["message"]["parts"][0]["text"]
        if text != "sum=42": raise AssertionError(f"unexpected result: {text!r}")
        print("PASS  client -> orchestrator -> Registry discovery -> downstream provider")
        print("RESULT: sum=42")
    finally: await agent.close()
if __name__=="__main__": asyncio.run(main())
