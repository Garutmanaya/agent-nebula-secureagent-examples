"""Verify native A2A push configuration CRUD and callback delivery."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import annotations
import asyncio
import os
from pathlib import Path
from fastapi import FastAPI, Request
import uvicorn
from a2a.helpers import new_text_message
from a2a.types import (DeleteTaskPushNotificationConfigRequest, GetTaskPushNotificationConfigRequest, ListTaskPushNotificationConfigsRequest, Role, SendMessageRequest, TaskPushNotificationConfig)
from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
SERVER_URL = "http://localhost:9019/"
CALLBACK_PORT = 9119
CALLBACK_TOKEN = "example-19-token"

# -----------------------------------------------------------------------------
# Push callback
# -----------------------------------------------------------------------------
notifications: list[dict] = []
callback_app = FastAPI()

@callback_app.post("/a2a/push")
async def receive_push(request: Request) -> dict[str, bool]:
    if request.headers.get("X-A2A-Notification-Token") != CALLBACK_TOKEN:
        raise AssertionError("push notification token mismatch")
    notifications.append(await request.json())
    return {"accepted": True}

async def _start_callback() -> tuple[uvicorn.Server, asyncio.Task]:
    server = uvicorn.Server(uvicorn.Config(callback_app, host="0.0.0.0", port=CALLBACK_PORT, log_level="warning"))
    task = asyncio.create_task(server.serve())
    while not server.started:
        await asyncio.sleep(0.02)
    return server, task

# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------
async def main() -> None:
    callback_server, callback_task = await _start_callback()
    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))
    client = await agent.a2a_client(SERVER_URL)
    try:
        stream = client.send_message(SendMessageRequest(message=new_text_message("long report", role=Role.ROLE_USER)))
        first = await anext(stream)
        if not first.HasField("task"):
            raise AssertionError(f"expected initial Task event, got {first}")
        task_id = first.task.id
        callback_host = os.environ.get("AGENT_HOSTNAME") or "localhost"
        created = await client.create_task_push_notification_config(TaskPushNotificationConfig(id="example-19", task_id=task_id, url=f"http://{callback_host}:{CALLBACK_PORT}/a2a/push", token=CALLBACK_TOKEN))
        if created.id != "example-19":
            raise AssertionError(f"unexpected push config: {created}")
        fetched = await client.get_task_push_notification_config(GetTaskPushNotificationConfigRequest(task_id=task_id, id=created.id))
        if fetched.url != created.url:
            raise AssertionError("get push config mismatch")
        listed = await client.list_task_push_notification_configs(ListTaskPushNotificationConfigsRequest(task_id=task_id, page_size=10))
        if created.id not in {item.id for item in listed.configs}:
            raise AssertionError("list push configs did not contain created config")
        print("PASS  native create/get/list push notification configuration")
        async for _ in stream:
            pass
        for _ in range(50):
            if notifications:
                break
            await asyncio.sleep(0.05)
        if not notifications:
            raise AssertionError("no push notification callback was delivered")
        print(f"PASS  native push callback delivery ({len(notifications)} notification(s))")
        await client.delete_task_push_notification_config(DeleteTaskPushNotificationConfigRequest(task_id=task_id, id=created.id))
        print("PASS  native delete push notification configuration")
        print("RESULT: Example 19 native A2A push notification verification passed")
    finally:
        await agent.close()
        callback_server.should_exit = True
        await callback_task

# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
