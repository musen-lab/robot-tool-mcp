"""Tests for the async subprocess runner."""

import asyncio

import pytest

from robot_mcp._runner import run_robot


class TestRunRobot:
    """Tests for run_robot."""

    def test_help_command(self, require_robot: None) -> None:
        """Running robot help succeeds."""
        result = asyncio.run(run_robot(["help"]))
        assert result["success"] is True
        assert result["exit_code"] == 0
        assert "usage: robot" in result["stdout"]
        assert result["command"] == "robot help"

    def test_version_command(self, require_robot: None) -> None:
        """Running robot --version succeeds."""
        result = asyncio.run(run_robot(["--version"]))
        assert result["success"] is True
        assert "ROBOT version" in result["stdout"]

    def test_invalid_command(self, require_robot: None) -> None:
        """Running an invalid command returns failure."""
        result = asyncio.run(run_robot(["nonexistent-command"]))
        assert result["success"] is False
        assert result["exit_code"] != 0

    def test_command_string_included(self, require_robot: None) -> None:
        """The command string is included in the result."""
        result = asyncio.run(run_robot(["help"]))
        assert result["command"] == "robot help"

    def test_missing_robot_binary(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Returns error when robot is not on PATH."""
        monkeypatch.setattr("robot_mcp._runner.shutil.which", lambda _: None)
        result = asyncio.run(run_robot(["help"]))
        assert result["success"] is False
        assert result["exit_code"] == -1
        assert "not found" in result["stderr"]
