"""Resolve initialized configuration paths for SecureAgent examples."""

from __future__ import annotations

import os
from pathlib import Path

_CONFIG_DIR_ENV = "AGENT_NEBULA_EXAMPLE_CONFIG_DIR"

def config_path(example_dir: Path, filename: str) -> Path:
    """Return external initialized config, or the checked-in config template for direct inspection."""
    configured = os.environ.get(_CONFIG_DIR_ENV)
    if configured:
        return Path(configured).expanduser().resolve() / filename
    return example_dir / "config" / filename
