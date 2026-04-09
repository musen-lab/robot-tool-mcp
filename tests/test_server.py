"""Tests for server setup and tool registration."""

from robot_mcp.server import mcp


class TestServerSetup:
    """Tests for the FastMCP server configuration."""

    def test_server_name(self) -> None:
        """Server has the correct name."""
        assert mcp.name == "robot-mcp"

    def test_instructions_set(self) -> None:
        """Server instructions are not empty."""
        assert mcp.instructions
        assert "ROBOT" in mcp.instructions

    def test_help_hint_in_instructions(self) -> None:
        """Server instructions include the --help discovery hint."""
        assert "--help" in mcp.instructions
