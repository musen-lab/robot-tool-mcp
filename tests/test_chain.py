"""Tests for the robot_chain tool."""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from robot_mcp.commands.chain import robot_chain


class TestChainArgBuilding:
    """Tests for chain tool argument construction (mocked subprocess)."""

    @patch("robot_mcp.commands.chain.run_robot", new_callable=AsyncMock)
    def test_single_step(self, mock_run: AsyncMock) -> None:
        """Single step produces correct args."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_chain(steps=[{"command": "merge", "input": ["a.owl"]}]))
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args == ["merge", "--input", "a.owl"]

    @patch("robot_mcp.commands.chain.run_robot", new_callable=AsyncMock)
    def test_multiple_steps(self, mock_run: AsyncMock) -> None:
        """Multiple steps are chained in order."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_chain(
                steps=[
                    {"command": "merge", "input": ["a.owl", "b.owl"]},
                    {"command": "reason", "reasoner": "ELK"},
                    {"command": "convert", "output": "result.owl"},
                ]
            )
        )
        args = mock_run.call_args[0][0]
        assert args == [
            "merge",
            "--input",
            "a.owl",
            "--input",
            "b.owl",
            "reason",
            "--reasoner",
            "ELK",
            "convert",
            "--output",
            "result.owl",
        ]

    @patch("robot_mcp.commands.chain.run_robot", new_callable=AsyncMock)
    def test_underscore_to_hyphen(self, mock_run: AsyncMock) -> None:
        """Underscores in keys become hyphens in flags."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_chain(
                steps=[
                    {
                        "command": "annotate",
                        "ontology_iri": "https://example.org/test.owl",
                    }
                ]
            )
        )
        args = mock_run.call_args[0][0]
        assert "--ontology-iri" in args
        assert "https://example.org/test.owl" in args

    @patch("robot_mcp.commands.chain.run_robot", new_callable=AsyncMock)
    def test_bool_values(self, mock_run: AsyncMock) -> None:
        """Boolean values become 'true'/'false' strings."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_chain(
                steps=[
                    {
                        "command": "reason",
                        "create_new_ontology": True,
                        "exclude_owl_thing": False,
                    }
                ]
            )
        )
        args = mock_run.call_args[0][0]
        assert args == [
            "reason",
            "--create-new-ontology",
            "true",
            "--exclude-owl-thing",
            "false",
        ]

    @patch("robot_mcp.commands.chain.run_robot", new_callable=AsyncMock)
    def test_list_values_repeat_flag(self, mock_run: AsyncMock) -> None:
        """List values produce repeated flags."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_chain(
                steps=[{"command": "merge", "input": ["a.owl", "b.owl", "c.owl"]}]
            )
        )
        args = mock_run.call_args[0][0]
        assert args == [
            "merge",
            "--input",
            "a.owl",
            "--input",
            "b.owl",
            "--input",
            "c.owl",
        ]

    @patch("robot_mcp.commands.chain.run_robot", new_callable=AsyncMock)
    def test_none_values_skipped(self, mock_run: AsyncMock) -> None:
        """None values are excluded from args."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_chain(
                steps=[{"command": "merge", "input": ["a.owl"], "output": None}]
            )
        )
        args = mock_run.call_args[0][0]
        assert "--output" not in args

    @patch("robot_mcp.commands.chain.run_robot", new_callable=AsyncMock)
    def test_global_options_prepended(self, mock_run: AsyncMock) -> None:
        """Global options appear before the first command."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_chain(
                steps=[{"command": "merge", "input": ["a.owl"]}],
                catalog="catalog.xml",
                verbose=True,
            )
        )
        args = mock_run.call_args[0][0]
        assert args == [
            "--catalog",
            "catalog.xml",
            "--verbose",
            "merge",
            "--input",
            "a.owl",
        ]

    @patch("robot_mcp.commands.chain.run_robot", new_callable=AsyncMock)
    def test_working_directory_passed(self, mock_run: AsyncMock) -> None:
        """Working directory is forwarded to run_robot."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_chain(
                steps=[{"command": "help"}],
                working_directory="/tmp",
            )
        )
        assert mock_run.call_args[1]["cwd"] == "/tmp"

    def test_missing_command_key(self) -> None:
        """Step without 'command' key returns error."""
        result = asyncio.run(robot_chain(steps=[{"input": ["a.owl"]}]))
        assert result["success"] is False
        assert "command" in result["stderr"].lower()

    @patch("robot_mcp.commands.chain.run_robot", new_callable=AsyncMock)
    def test_int_values_converted(self, mock_run: AsyncMock) -> None:
        """Integer values are converted to strings."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_chain(steps=[{"command": "collapse", "threshold": 3}]))
        args = mock_run.call_args[0][0]
        assert args == ["collapse", "--threshold", "3"]

    @patch("robot_mcp.commands.chain.run_robot", new_callable=AsyncMock)
    def test_help_flag_via_chain(self, mock_run: AsyncMock) -> None:
        """Help can be requested via chain step."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_chain(steps=[{"command": "merge", "help": True}]))
        args = mock_run.call_args[0][0]
        assert args == ["merge", "--help", "true"]


class TestChainIntegration:
    """Integration tests that run actual ROBOT commands."""

    def test_chain_help(self, require_robot: None) -> None:
        """Chaining a help command succeeds."""
        result = asyncio.run(robot_chain(steps=[{"command": "help"}]))
        assert result["success"] is True
        assert "usage: robot" in result["stdout"]

    def test_chain_merge_annotate_convert(
        self, require_robot: None, tmp_path: pytest.TempPathFactory
    ) -> None:
        """Chain merge -> annotate -> convert produces an output file."""
        output = str(tmp_path / "result.owl")
        result = asyncio.run(
            robot_chain(
                steps=[
                    {"command": "merge", "input": ["/dev/null"]},
                    {
                        "command": "annotate",
                        "ontology_iri": "https://example.org/test.owl",
                    },
                    {"command": "convert", "output": output},
                ]
            )
        )
        assert result["success"] is True
        import os

        assert os.path.exists(output)
