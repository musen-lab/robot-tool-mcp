"""ROBOT command tools — each module registers one MCP tool."""

from fastmcp import FastMCP

from robot_mcp.commands.chain import robot_chain


def register_all(mcp: FastMCP) -> None:
    """Register every ROBOT command tool on the given server."""
    mcp.tool(robot_chain)
