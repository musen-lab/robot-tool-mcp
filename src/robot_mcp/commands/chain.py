"""The robot_chain tool — execute a pipeline of ROBOT commands in one process."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_chain(
    steps: list[dict[str, Any]],
    working_directory: str | None = None,
    catalog: str | None = None,
    prefixes: str | None = None,
    add_prefix: list[str] | None = None,
    noprefixes: bool = False,
    verbose: bool = False,
    strict: bool = False,
    xml_entities: bool = False,
) -> dict[str, Any]:
    """Execute a chain of ROBOT commands in a single process.

    Ontology objects pass in-memory between steps — much more efficient
    than writing intermediate files.  Only the first step typically needs
    an ``input`` key and only the last step needs an ``output`` key.

    Each step is a dict with:
      - ``command``: the ROBOT command name (e.g. "merge", "reason")
      - All other keys are command arguments.  Use the long flag name
        without leading dashes, with hyphens replaced by underscores.

    Argument mapping rules:
      - Underscores become hyphens: ``ontology_iri`` → ``--ontology-iri``
      - ``list`` values repeat the flag: ``{"input": ["a.owl", "b.owl"]}``
        → ``--input a.owl --input b.owl``
      - ``bool`` values become ``"true"`` / ``"false"`` strings
      - ``str`` / ``int`` values become a single flag-value pair

    Example steps::

        [
            {"command": "merge", "input": ["edit.owl", "base.owl"]},
            {"command": "reason", "reasoner": "ELK"},
            {"command": "annotate", "ontology_iri": "https://example.org/my.owl"},
            {"command": "convert", "format": "ofn", "output": "result.owl"}
        ]

    Tip: to discover available flags for a command, pass ``"help": true``
    in a step, e.g. ``[{"command": "merge", "help": true}]``.
    """
    args = build_global_args(
        catalog=catalog,
        prefixes=prefixes,
        add_prefix=add_prefix,
        noprefixes=noprefixes,
        verbose=verbose,
        strict=strict,
        xml_entities=xml_entities,
    )

    for step in steps:
        step = dict(step)  # copy so we don't mutate the caller's data
        command = step.pop("command", None)
        if not command:
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": "Each step must have a 'command' key.",
                "command": "",
            }
        args.append(command)

        for key, value in step.items():
            flag = "--" + key.replace("_", "-")
            if isinstance(value, bool):
                args.extend([flag, "true" if value else "false"])
            elif isinstance(value, list):
                for v in value:
                    args.extend([flag, str(v)])
            elif value is not None:
                args.extend([flag, str(value)])

    return await run_robot(args, cwd=working_directory)
