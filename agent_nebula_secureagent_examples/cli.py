"""Copy the packaged examples into an editable working directory."""
from __future__ import annotations

import argparse
import shutil
from importlib.resources import files
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Install the Agent Nebula example workspace")
    parser.add_argument("command", choices=["init"], help="Copy the examples into a directory")
    parser.add_argument("destination", type=Path, help="Destination directory (must not exist)")
    args = parser.parse_args()

    target = args.destination.expanduser().resolve()
    if target.exists():
        parser.error(f"Destination already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)

    source = files("agent_nebula_secureagent_examples").joinpath("assets")
    with source.joinpath("README.md").open("rb"):
        pass
    try:
        shutil.copytree(str(source), target)
    except Exception:
        if target.exists():
            shutil.rmtree(target)
        raise
    # The original repository uses uv; the copied workspace resolves SecureAgent
    # from PyPI, not from a sibling source checkout.
    (target / "pyproject.toml").write_text(
        '[project]\\n'
        'name = "agent-nebula-secureagent-examples-workspace"\\n'
        'version = "0.0.0"\\n'
        'requires-python = ">=3.12"\\n'
        'dependencies = ["agent-nebula-secureagent[a2a-grpc]>=5.0.0,<6.0.0"]\\n'
        '\\n[dependency-groups]\\n'
        'dev = ["ruff>=0.12,<1.0"]\\n'
    )
    print(f"Example workspace created: {target}")
    print(f"Next: cd {target} && make install && make env-init && make list")
