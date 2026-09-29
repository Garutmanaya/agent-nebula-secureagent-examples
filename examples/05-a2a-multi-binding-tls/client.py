"""Verify every skill over JSON-RPC/HTTPS, HTTP+JSON/HTTPS, and gRPC/TLS."""
import asyncio
from pathlib import Path

from examples.example_paths import config_path
from agent_nebula_secureagent import DiscoveredAgent, SecureAgent
HERE=Path(__file__).resolve().parent
SERVER_URL="https://localhost:9005/"
BINDINGS=(("JSON-RPC","a2aclient-jsonrpc.conf"),("HTTP+JSON","a2aclient-http-json.conf"),("gRPC","a2aclient-grpc.conf"))

SKILL_CASES = (
    ("hello", {"name": "Agent Nebula"}, "hello from SecureAgent"),
    ("echo", {"value": "registry"}, "echo=registry"),
    ("add", {"a": 7, "b": 5}, "sum=12"),
)

def _direct_provider(agent_card: dict, agent_card_url: str) -> DiscoveredAgent:
    """Adapt direct Agent Card discovery to the current SecureAgent invocation API."""
    return DiscoveredAgent(
        agent_id=str(agent_card.get("name") or agent_card_url),
        display_name=str(agent_card.get("name") or agent_card_url),
        agent_card_url=agent_card_url,
    )


def response_text(responses):
    if len(responses) != 1:
        raise AssertionError(f"expected one response, got {len(responses)}")
    message = responses[0].get("message")
    if not isinstance(message, dict):
        raise AssertionError(f"missing A2A message: {responses[0]}")
    parts = message.get("parts")
    if not isinstance(parts, list) or not parts or not isinstance(parts[0], dict):
        raise AssertionError(f"missing A2A message parts: {message}")
    text = parts[0].get("text")
    if not isinstance(text, str):
        raise AssertionError(f"missing text response: {parts[0]}")
    return text

async def main():
    total=0
    for label, config in BINDINGS:
        agent=SecureAgent(config=config_path(HERE, "secureagent.conf"))
        agent.use_protocol("a2a",role="client",config=config_path(HERE, config))
        try:
            card = await agent.resolve_agent_card(SERVER_URL)
            provider = _direct_provider(card, SERVER_URL)
            for skill_id,data,expected in SKILL_CASES:
                actual=response_text(await agent.send_message(provider,data=data,skill_id=skill_id))
                if actual != expected: raise AssertionError(f"{label}/{skill_id}: {actual!r} != {expected!r}")
                print(f"PASS  {label:<10} {skill_id}")
                total += 1
        finally: await agent.close()
    print(f"RESULT: {total}/9 TLS binding/skill invocations passed")
if __name__=="__main__": asyncio.run(main())
