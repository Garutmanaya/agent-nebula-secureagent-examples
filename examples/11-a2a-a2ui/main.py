"""A2A + A2UI v1.0 acceptance server."""
from pathlib import Path

from examples.example_paths import config_path

from agent_nebula_secureagent import SecureAgent, SkillResult

HERE = Path(__file__).resolve().parent

agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    a2ui_config=config_path(HERE, "a2ui.conf"),
)
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))


@agent.skill("summary")
async def summary(payload):
    """Return a conventional non-A2UI result for fallback verification."""
    return {"message": "summary ready", "items": 3}


@agent.skill("forecast")
async def forecast(payload):
    """Return business data, result metadata, and an A2UI v1.0 surface."""
    region = str(payload.get("region", "global"))
    return SkillResult(
        data={
            "message": f"forecast ready for {region}",
            "region": region,
            "units": 1250,
        },
        metadata={"source": "example-11", "resultType": "forecast"},
        ui={
            "surface_id": "forecast-surface",
            "messages": (
                {
                    "document": {
                        "version": "v1.0",
                        "createSurface": {
                            "surfaceId": "forecast-surface",
                            "dataModel": {
                                "region": region,
                                "units": 1250,
                            },
                        },
                    }
                },
            ),
            "metadata": {"purpose": "acceptance-test"},
        },
    )


if __name__ == "__main__":
    agent.run()
