"""FastMCP server for the ROBOT ontology CLI tool."""

from fastmcp import FastMCP

from robot_mcp.commands import register_all

mcp = FastMCP(
    "robot-mcp",
    instructions=(
        "MCP server for ROBOT, the OWL ontology CLI tool "
        "(https://robot.obolibrary.org/). "
        "Use individual command tools for single operations, or use "
        "robot_chain to efficiently pipeline multiple commands in a single "
        "ROBOT invocation where ontology objects pass in-memory between steps. "
        "Common workflow: merge -> reason -> annotate -> convert."
    ),
)

register_all(mcp)


def main() -> None:
    """Entry point for ``uvx robot-mcp``."""
    mcp.run()
