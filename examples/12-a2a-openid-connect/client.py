"""Verify OpenID Connect authentication through the native a2a-sdk client."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from __future__ import annotations

import asyncio
import uuid
from pathlib import Path

from a2a.helpers import get_message_text
from a2a.types import Message, Part, Role, SendMessageRequest
from google.protobuf.json_format import ParseDict
from google.protobuf.struct_pb2 import Struct, Value

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent

# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
SERVER_URL = "https://localhost:9012/"

# -----------------------------------------------------------------------------
# A2A request helpers
# -----------------------------------------------------------------------------

def _data_part(data: dict[str, object]) -> Part:
    return Part(data=Value(struct_value=ParseDict(data, Struct())))


# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------

async def main() -> None:
    # Test-only credential provisioning. A2A advertises OIDC but does not issue
    # identity tokens; production credentials come from the configured IdP.
    import os
    import time
    import jwt

    config_dir = Path(os.environ["AGENT_NEBULA_EXAMPLE_CONFIG_DIR"])
    runtime = config_dir.parent
    now = int(time.time())
    token = jwt.encode(
        {"iss": "https://issuer.example", "sub": "example-client", "aud": "a2a-example", "iat": now, "exp": now + 300},
        (runtime / "certs/client.key").read_text(encoding="utf-8"),
        algorithm="RS256",
        headers={"kid": "example-oidc-key"},
    )
    (runtime / "secrets/oidc-token").write_text(token, encoding="utf-8")

    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))
    try:
        card = await agent.resolve_agent_card(SERVER_URL)
        if {skill.id for skill in card.skills} != {"hello"}:
            raise AssertionError("Agent Card must advertise only the hello skill")
        if "oidc" not in card.security_schemes:
            raise AssertionError("Agent Card is missing oidc security scheme")
        client = await agent.a2a_client(SERVER_URL)
        request = SendMessageRequest(message=Message(role=Role.ROLE_USER, message_id=str(uuid.uuid4()), parts=[_data_part({"name": "Agent Nebula"})]))
        responses = [event async for event in client.send_message(request)]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(f"expected one Message response: {responses}")
        actual = get_message_text(responses[0].message, delimiter=" ")
        if actual != "authenticated hello":
            raise AssertionError(f"unexpected response: {actual!r}")
        print("PASS  OIDC authenticated A2A invocation")
    finally:
        await agent.close()


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
