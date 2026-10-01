"""A2UI v1.0 bidirectional action example server."""
from pathlib import Path
from collections.abc import Mapping

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent, SkillResult

HERE = Path(__file__).resolve().parent
SURFACE_ID = "forecast-action-surface"

# Configure SecureAgent from the generated runtime configuration.
agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    a2ui_config=config_path(HERE, "a2ui.conf"),
)
# Enable the A2A server role using the example-specific protocol config.
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))


def _initial_surface(units: int):
    return {
        "surface_id": SURFACE_ID,
        "messages": (
            {
                "document": {
                    "version": "v1.0",
                    "createSurface": {
                        "surfaceId": SURFACE_ID,
                        "sendDataModel": True,
                        "components": [
                            {"id": "root", "component": "Column", "children": ["value", "button"]},
                            {"id": "value", "component": "Text", "text": str(units)},
                            {
                                "id": "button",
                                "component": "Button",
                                "child": "button-label",
                                "action": {"event": {"name": "recalculate", "context": {"delta": 50}}},
                            },
                            {"id": "button-label", "component": "Text", "text": "Recalculate"},
                        ],
                        "dataModel": {"units": units},
                    },
                }
            },
        ),
    }


@agent.skill("forecast")
async def forecast(payload):
    """Create the surface or process a renderer-originated A2UI action."""
    action = payload.get("a2ui_action")
    if not isinstance(action, Mapping):
        return SkillResult(
            data={"units": 1250, "state": "initial"},
            ui=_initial_surface(1250),
        )

    if action.get("name") != "recalculate":
        raise ValueError(f"unexpected A2UI action: {action.get('name')}")
    renderer_model = payload.get("a2ui_renderer_data_model", {})
    surfaces = renderer_model.get("surfaces", {}) if isinstance(renderer_model, Mapping) else {}
    current = surfaces.get(SURFACE_ID, {}) if isinstance(surfaces, Mapping) else {}
    units = int(current.get("units", 1250)) + int(action.get("context", {}).get("delta", 0))
    action_id = action.get("action_id")
    return SkillResult(
        data={"units": units, "state": "recalculated"},
        ui={
            "surface_id": SURFACE_ID,
            "messages": (
                {
                    "document": {
                        "version": "v1.0",
                        "actionId": action_id,
                        "actionResponse": {"value": {"units": units}},
                    }
                },
                {
                    "document": {
                        "version": "v1.0",
                        "updateDataModel": {
                            "surfaceId": SURFACE_ID,
                            "path": "/units",
                            "value": units,
                        },
                    }
                },
            ),
        },
    )


if __name__ == "__main__":
    print("START: SecureAgent A2A example server")
    agent.run()
