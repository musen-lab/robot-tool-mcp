"""ROBOT unmerge command — remove axioms of one ontology from another."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_unmerge(
    input: list[str] | None = None,
    output: str | None = None,
    working_directory: str | None = None,
    catalog: str | None = None,
    prefixes: str | None = None,
    add_prefix: list[str] | None = None,
    noprefixes: bool = False,
    verbose: bool = False,
    strict: bool = False,
    xml_entities: bool = False,
    extra_args: list[str] | None = None,  # use ["--help"] to list available flags
) -> dict[str, Any]:
    """Remove axioms from the first ontology that appear in subsequent ontologies.

    Provide multiple ``input`` files: the first is the base ontology, and
    axioms from the remaining inputs are subtracted from it.
    """
    args = build_global_args(
        catalog=catalog, prefixes=prefixes, add_prefix=add_prefix,
        noprefixes=noprefixes, verbose=verbose, strict=strict,
        xml_entities=xml_entities,
    )
    args.append("unmerge")
    if input:
        for i in input:
            args.extend(["--input", i])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
