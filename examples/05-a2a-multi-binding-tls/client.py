"""Verify every skill over JSON-RPC/HTTPS, HTTP+JSON/HTTPS, and gRPC/TLS."""
import asyncio
from pathlib import Path
from agent_nebula_secureagent import SecureAgent
HERE=Path(__file__).resolve().parent
SERVER_URL="https://localhost:9005/"
BINDINGS=(("JSON-RPC","a2aclient-jsonrpc.conf"),("HTTP+JSON","a2aclient-http-json.conf"),("gRPC","a2aclient-grpc.conf"))

SKILL_CASES = (
    ("hello", {"name": "Agent Nebula"}, "hello from SecureAgent"),
    ("echo", {"value": "registry"}, "echo=registry"),
    ("add", {"a": 7, "b": 5}, "sum=12"),
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
        agent=SecureAgent(config=HERE/"secureagent.conf")
        agent.use_protocol("a2a",role="client",config=HERE/config)
        try:
            for skill_id,data,expected in SKILL_CASES:
                actual=response_text(await agent.send_message_to(SERVER_URL,data=data,skill_id=skill_id))
                if actual != expected: raise AssertionError(f"{label}/{skill_id}: {actual!r} != {expected!r}")
                print(f"PASS  {label:<10} {skill_id}")
                total += 1
        finally: await agent.close()
    print(f"RESULT: {total}/9 TLS binding/skill invocations passed")
if __name__=="__main__": asyncio.run(main())
