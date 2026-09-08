"""Resolve generated configuration paths for SecureAgent examples."""

from __future__ import annotations

import os
from pathlib import Path


_CONFIG_DIR_ENV = "AGENT_NEBULA_EXAMPLE_CONFIG_DIR"


def config_path(example_dir: Path, filename: str) -> Path:
    """Return the initialized config path, falling back to the source example."""
    configured = os.environ.get(_CONFIG_DIR_ENV)
    if configured:
        return Path(configured).expanduser().resolve() / filename
    return example_dir / filename
