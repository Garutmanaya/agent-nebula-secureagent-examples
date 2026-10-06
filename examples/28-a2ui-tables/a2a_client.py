from __future__ import annotations
from pathlib import Path
from a2a.client import ClientCallContext
from a2a.client.service_parameters import ServiceParametersFactory, with_a2a_extensions
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.struct_pb2 import Struct
from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path
RICH_CATALOG_ID = "https://agentnebula.ai/catalogs/a2ui/rich/v1/catalog.json"
def discover_extensions(card, need_dispatch=False):
    a2ui=[]; other=[]
    for extension in card.capabilities.extensions:
        params=MessageToDict(extension.params) if extension.HasField("params") else {}
        (a2ui if "supportedCatalogIds" in params.get("v1.0", {}) else other).append(extension.uri)
    if len(a2ui)!=1 or (need_dispatch and len(other)!=1): raise AssertionError(f"unexpected extensions: a2ui={a2ui}, other={other}")
    return a2ui[0], (other[0] if need_dispatch else None)

SERVER_URL="http://localhost:9028/"
async def request_surface(here: Path)->dict:
    agent=SecureAgent(config=config_path(here,"secureagent.conf"),a2ui_config=config_path(here,"a2ui.conf")); agent.use_protocol("a2a",role="client",config=config_path(here,"a2aclient.conf"))
    card=await agent.resolve_agent_card(SERVER_URL); a2ui_uri,_=discover_extensions(card)
    metadata=ParseDict({"a2uiRendererCapabilities":{"v1.0":{"supportedCatalogIds":[RICH_CATALOG_ID]}}},Struct())
    request=SendMessageRequest(message=new_text_message("show inventory table",role=Role.ROLE_USER),metadata=metadata)
    context=ClientCallContext(service_parameters=ServiceParametersFactory.create([with_a2a_extensions([a2ui_uri])]))
    client=await agent.a2a_client(SERVER_URL)
    try:
        responses=[event async for event in client.send_message(request,context=context)]
        return MessageToDict(responses[0].message,preserving_proto_field_name=True)
    finally: await agent.close()
