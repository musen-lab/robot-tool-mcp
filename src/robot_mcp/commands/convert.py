"""ROBOT convert command — transform ontology between file formats."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import StrOrList, build_global_args, ensure_list


async def robot_convert(
    input: str | None = None,
    output: str | None = None,
    format: str | None = None,
    check: bool | None = None,
    working_directory: str | None = None,
    catalog: str | None = None,
    prefixes: str | None = None,
    add_prefix: StrOrList = None,
    noprefixes: bool = False,
    verbose: bool = False,
    strict: bool = False,
    xml_entities: bool = False,
    extra_args: StrOrList = None,
) -> dict[str, Any]:
    """Convert an ontology between formats.

    Supported formats (by extension or ``format`` flag): owl (RDF/XML),
    ofn (OWL Functional), omn (Manchester), owx (OWL/XML), ttl (Turtle),
    obo (OBO Format), json (OBO Graphs JSON).  Gzip compression is
    supported by appending ``.gz`` to the output path.
    """
    add_prefix = ensure_list(add_prefix)
    extra_args = ensure_list(extra_args)
    args = build_global_args(
        catalog=catalog,
        prefixes=prefixes,
        add_prefix=add_prefix,
        noprefixes=noprefixes,
        verbose=verbose,
        strict=strict,
        xml_entities=xml_entities,
    )
    args.append("convert")
    if input:
        args.extend(["--input", input])
    if format:
        args.extend(["--format", format])
    if check is not None:
        args.extend(["--check", str(check).lower()])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
