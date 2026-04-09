"""ROBOT measure command — compute ontology metrics."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_measure(
    input: str | None = None,
    output: str | None = None,
    metrics: str = "essential",
    format: str | None = None,
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
    """Compute ontology metrics (entity counts, axiom counts, complexity).

    Metric sets: ``essential`` (default), ``extended``, ``all``,
    ``reasoner-essential``, ``reasoner-extended``, ``reasoner-all``.
    Output formats: tsv, csv, json, yaml, html.
    """
    args = build_global_args(
        catalog=catalog, prefixes=prefixes, add_prefix=add_prefix,
        noprefixes=noprefixes, verbose=verbose, strict=strict,
        xml_entities=xml_entities,
    )
    args.append("measure")
    if input:
        args.extend(["--input", input])
    args.extend(["--metrics", metrics])
    if format:
        args.extend(["--format", format])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
