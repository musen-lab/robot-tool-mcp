"""Shared fixtures for robot-mcp tests."""

import shutil

import pytest


@pytest.fixture
def has_robot() -> bool:
    """Check if the robot CLI is available."""
    return shutil.which("robot") is not None


@pytest.fixture
def require_robot(has_robot: bool) -> None:
    """Skip test if robot CLI is not installed."""
    if not has_robot:
        pytest.skip("robot CLI not found on PATH")
