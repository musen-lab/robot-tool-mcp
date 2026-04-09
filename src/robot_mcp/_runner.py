"""Async subprocess runner for the ROBOT CLI."""

import asyncio
import shutil
from typing import Any


async def run_robot(args: list[str], cwd: str | None = None) -> dict[str, Any]:
    """Execute a robot CLI command and return structured results.

    Args:
        args: Command arguments (without the leading "robot").
        cwd: Working directory for the command.

    Returns:
        Dict with keys: success, exit_code, stdout, stderr, command.
    """
    robot_bin = shutil.which("robot")
    if robot_bin is None:
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": "robot executable not found on PATH",
            "command": f"robot {' '.join(args)}",
        }

    proc = await asyncio.create_subprocess_exec(
        robot_bin,
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
    )
    stdout, stderr = await proc.communicate()

    return {
        "success": proc.returncode == 0,
        "exit_code": proc.returncode,
        "stdout": stdout.decode("utf-8", errors="replace"),
        "stderr": stderr.decode("utf-8", errors="replace"),
        "command": f"robot {' '.join(args)}",
    }
