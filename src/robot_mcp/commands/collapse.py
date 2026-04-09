"""ROBOT collapse command — simplify class hierarchies."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_collapse(
    input: str | None = None,
    output: str | None = None,
    threshold: int | None = None,
    precious: list[str] | None = None,
    precious_terms: str | None = None,
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
    """Collapse class hierarchies by removing intermediate classes.

    Classes with fewer than ``threshold`` (default 2) subclasses are
    removed, and their subclasses are promoted.  Use ``precious`` or
    ``precious_terms`` to protect specific classes from removal.
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
    args.append("collapse")
    if input:
        args.extend(["--input", input])
    if threshold is not None:
        args.extend(["--threshold", str(threshold)])
    if precious:
        for p in precious:
            args.extend(["--precious", p])
    if precious_terms:
        args.extend(["--precious-terms", precious_terms])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
