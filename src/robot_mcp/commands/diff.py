"""ROBOT diff command — compare two ontologies."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import StrOrList, build_global_args, ensure_list


async def robot_diff(
    left: str | None = None,
    right: str | None = None,
    left_iri: str | None = None,
    right_iri: str | None = None,
    left_catalog: str | None = None,
    right_catalog: str | None = None,
    output: str | None = None,
    format: str | None = None,
    labels: bool | None = None,
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
    """Compare two ontologies and report semantic differences.

    Specify ontologies via file paths (``left``/``right``) or IRIs
    (``left_iri``/``right_iri``).  Output formats: plain (default),
    pretty, html, markdown.  Use ``labels`` to include human-readable
    entity labels in the diff output.
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
    args.append("diff")
    if left:
        args.extend(["--left", left])
    if right:
        args.extend(["--right", right])
    if left_iri:
        args.extend(["--left-iri", left_iri])
    if right_iri:
        args.extend(["--right-iri", right_iri])
    if left_catalog:
        args.extend(["--left-catalog", left_catalog])
    if right_catalog:
        args.extend(["--right-catalog", right_catalog])
    if format:
        args.extend(["--format", format])
    if labels is not None:
        args.extend(["--labels", str(labels).lower()])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
