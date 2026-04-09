"""ROBOT command tools — each module registers one MCP tool."""

from fastmcp import FastMCP

from robot_mcp.commands.annotate import robot_annotate
from robot_mcp.commands.chain import robot_chain
from robot_mcp.commands.convert import robot_convert
from robot_mcp.commands.extract import robot_extract
from robot_mcp.commands.filter import robot_filter
from robot_mcp.commands.merge import robot_merge
from robot_mcp.commands.reason import robot_reason
from robot_mcp.commands.reduce import robot_reduce
from robot_mcp.commands.relax import robot_relax
from robot_mcp.commands.remove import robot_remove
from robot_mcp.commands.rename import robot_rename
from robot_mcp.commands.unmerge import robot_unmerge


def register_all(mcp: FastMCP) -> None:
    """Register every ROBOT command tool on the given server."""
    mcp.tool(robot_chain)

    # Core ontology manipulation
    mcp.tool(robot_merge)
    mcp.tool(robot_unmerge)
    mcp.tool(robot_annotate)
    mcp.tool(robot_convert)
    mcp.tool(robot_reason)
    mcp.tool(robot_reduce)
    mcp.tool(robot_relax)

    # Extraction and filtering
    mcp.tool(robot_extract)
    mcp.tool(robot_filter)
    mcp.tool(robot_remove)
    mcp.tool(robot_rename)
