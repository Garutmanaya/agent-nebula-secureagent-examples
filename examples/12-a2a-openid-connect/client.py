"""A2A security example client."""
import asyncio
from pathlib import Path
from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent
HERE=Path(__file__).resolve().parent
SERVER_URL="https://localhost:9012/"
async def main():

    # This example acts as the external OIDC issuer only for deterministic local
    # test-token provisioning. A2A itself never issues OIDC credentials.
    import os, time, jwt
    config_dir=Path(os.environ["AGENT_NEBULA_EXAMPLE_CONFIG_DIR"])
    runtime=config_dir.parent
    token=jwt.encode({"iss":"https://issuer.example","sub":"example-client","aud":"a2a-example","iat":int(time.time()),"exp":int(time.time())+300}, (runtime/"certs/client.key").read_text(), algorithm="RS256", headers={"kid":"example-oidc-key"})
    (runtime/"secrets/oidc-token").write_text(token)
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
