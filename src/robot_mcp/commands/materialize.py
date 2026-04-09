"""ROBOT materialize command — assert inferred superclass relationships."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_materialize(
    input: str | None = None,
    output: str | None = None,
    reasoner: str = "ELK",
    term: list[str] | None = None,
    term_file: str | None = None,
    working_directory: str | None = None,
    catalog: str | None = None,
    prefixes: str | None = None,
    add_prefix: list[str] | None = None,
    noprefixes: bool = False,
    verbose: bool = False,
    strict: bool = False,
    xml_entities: bool = False,
    extra_args: list[str] | None = None,
) -> dict[str, Any]:
    """Materialize inferred superclass relationships using a reasoner.

    Similar to ``reason`` but focused on asserting existential
    restrictions.  Use ``term`` or ``term_file`` to restrict which
    properties to materialize.
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
    args.append("materialize")
    if input:
        args.extend(["--input", input])
    args.extend(["--reasoner", reasoner])
    if term:
        for t in term:
            args.extend(["--term", t])
    if term_file:
        args.extend(["--term-file", term_file])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
