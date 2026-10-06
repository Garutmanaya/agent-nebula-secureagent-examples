"""Native a2a-sdk single-skill invocation shared by CLI and browser clients."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import annotations

from pathlib import Path

from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest
from google.protobuf.json_format import MessageToDict

from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

SERVER_URL = "http://localhost:9023/"

# -----------------------------------------------------------------------------
# A2A request helper
# -----------------------------------------------------------------------------
async def request_dashboard(here: Path, text: str = "show weather dashboard") -> dict:
    """Invoke the example's single advertised skill through native a2a-sdk."""
    agent = SecureAgent(config=config_path(here, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(here, "a2aclient.conf"))
    request = SendMessageRequest(message=new_text_message(text, role=Role.ROLE_USER))
    client = await agent.a2a_client(SERVER_URL)
    try:
        responses = [event async for event in client.send_message(request)]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(f"expected one A2A Message: {responses}")
        return MessageToDict(responses[0].message, preserving_proto_field_name=True)
    finally:
        await agent.close()
