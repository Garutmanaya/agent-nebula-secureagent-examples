"""Verify authenticated retrieval through native Client.get_extended_agent_card()."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import annotations
import asyncio
from pathlib import Path
from a2a.types import GetExtendedAgentCardRequest
from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
SERVER_URL = "https://localhost:9020/"

# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------
async def main() -> None:
    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))
    public_card = await agent.resolve_agent_card(SERVER_URL)
    if not public_card.capabilities.extended_agent_card:
        raise AssertionError("public card does not advertise extended Agent Card support")
    if public_card.name != "Public Extended Card Agent":
        raise AssertionError(f"unexpected public card: {public_card.name}")
    print("PASS  public Agent Card advertises extended_agent_card=true")
    client = await agent.a2a_client(SERVER_URL)
    try:
        extended = await client.get_extended_agent_card(GetExtendedAgentCardRequest())
        if extended.name != "Authenticated Extended Card Agent":
            raise AssertionError(f"unexpected extended card: {extended.name}")
        if "private operational description" not in extended.description:
            raise AssertionError("extended card did not contain richer authenticated description")
        print("PASS  native client.get_extended_agent_card() returned authenticated card")
        print("RESULT: Example 20 native A2A Extended Agent Card verification passed")
    finally:
        await agent.close()

# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
