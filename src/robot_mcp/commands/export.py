"""ROBOT export command — generate tabular output from an ontology."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_export(
    input: str | None = None,
    header: str | None = None,
    export: str | None = None,
    format: str | None = None,
    sort: str | None = None,
    split: str | None = None,
    include: str | None = None,
    entity_select: str | None = None,
    entity_format: str | None = None,
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
    """Export ontology data to a table (CSV, TSV, JSON, HTML, XLSX).

    The ``header`` defines columns using pipe-separated names like
    ``"ID|LABEL|SubClass Of"``.  Use ``include`` to specify entity types
    (classes, individuals, properties).  Use ``sort`` to order by column.
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
    args.append("export")
    if input:
        args.extend(["--input", input])
    if header:
        args.extend(["--header", header])
    if export:
        args.extend(["--export", export])
    if format:
        args.extend(["--format", format])
    if sort:
        args.extend(["--sort", sort])
    if split:
        args.extend(["--split", split])
    if include:
        args.extend(["--include", include])
    if entity_select:
        args.extend(["--entity-select", entity_select])
    if entity_format:
        args.extend(["--entity-format", entity_format])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
