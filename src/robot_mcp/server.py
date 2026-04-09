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
        "Common workflow: merge -> reason -> annotate -> convert. "
        "\n\n"
        "IMPORTANT: Before using a flag you are not certain about, verify it "
        "exists by running the command with --help first. For example, use "
        'robot_chain with [{"command": "<command>", "help": true}] or use '
        'an individual tool with extra_args: ["--help"]. This avoids '
        "hallucinating flags that don't exist in the user's ROBOT version."
    ),
)

register_all(mcp)


def main() -> None:
    """Entry point for ``uvx robot-ontology-mcp``."""
    mcp.run()
