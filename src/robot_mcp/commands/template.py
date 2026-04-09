"""ROBOT template command — convert tabular data to OWL."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_template(
    input: str | None = None,
    output: str | None = None,
    template: list[str] | None = None,
    prefix: list[str] | None = None,
    ontology_iri: str | None = None,
    merge_before: bool | None = None,
    merge_after: bool | None = None,
    force: bool | None = None,
    errors: str | None = None,
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
    """Convert tabular data (CSV/TSV) into OWL ontology format.

    The template file has: row 1 = headers, row 2 = template strings
    (e.g. ``ID``, ``LABEL``, ``SC %`` for subclass), rows 3+ = data.
    Use ``merge_before`` or ``merge_after`` to control how template
    output combines with the input ontology.
    """
    args = build_global_args(
        catalog=catalog, prefixes=prefixes, add_prefix=add_prefix,
        noprefixes=noprefixes, verbose=verbose, strict=strict,
        xml_entities=xml_entities,
    )
    args.append("template")
    if input:
        args.extend(["--input", input])
    if template:
        for t in template:
            args.extend(["--template", t])
    if prefix:
        for p in prefix:
            args.extend(["--prefix", p])
    if ontology_iri:
        args.extend(["--ontology-iri", ontology_iri])
    if merge_before is not None:
        args.extend(["--merge-before", str(merge_before).lower()])
    if merge_after is not None:
        args.extend(["--merge-after", str(merge_after).lower()])
    if force is not None:
        args.extend(["--force", str(force).lower()])
    if errors:
        args.extend(["--errors", errors])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
