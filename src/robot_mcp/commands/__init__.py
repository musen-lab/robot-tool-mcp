"""ROBOT command tools — each module registers one MCP tool."""

from fastmcp import FastMCP


def register_all(mcp: FastMCP) -> None:
    """Register every ROBOT command tool on the given server."""
    # Will be populated as command modules are added.
    pass
