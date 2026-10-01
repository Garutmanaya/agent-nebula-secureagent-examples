"""A2A security example client."""
import asyncio
from pathlib import Path
from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent
HERE=Path(__file__).resolve().parent
SERVER_URL="https://localhost:9010/"
async def main():
    agent=SecureAgent(config=config_path(HERE,"secureagent.conf"))
    agent.use_protocol("a2a",role="client",config=config_path(HERE,"a2aclient.conf"))
    try:
        card=await agent.resolve_agent_card(SERVER_URL)
        print("Resolved:",card.name)
        result=await agent.send_message_to(SERVER_URL,data={"name":"Agent Nebula"})
        print("Result:",result)
    finally:
        await agent.close()
if __name__=="__main__": asyncio.run(main())
