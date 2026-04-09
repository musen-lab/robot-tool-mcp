"""ROBOT mirror command — cache imported ontologies locally."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_mirror(
    input: str | None = None,
    output: str | None = None,
    directory: str | None = None,
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
    """Mirror (cache) external ontology imports locally.

    Downloads all imported ontologies to ``directory`` and generates a
    catalog XML file at ``output`` for offline use.  Prevents network
    failures from breaking builds.
    """
    args = build_global_args(
        catalog=catalog, prefixes=prefixes, add_prefix=add_prefix,
        noprefixes=noprefixes, verbose=verbose, strict=strict,
        xml_entities=xml_entities,
    )
    args.append("mirror")
    if input:
        args.extend(["--input", input])
    if directory:
        args.extend(["--directory", directory])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
