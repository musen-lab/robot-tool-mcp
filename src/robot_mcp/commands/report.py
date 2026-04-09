"""ROBOT report command — run quality control checks on an ontology."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_report(
    input: str | None = None,
    output: str | None = None,
    fail_on: str | None = None,
    labels: bool | None = None,
    profile: str | None = None,
    limit: int | None = None,
    base_iri: str | None = None,
    tdb: bool | None = None,
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
    """Run quality control SPARQL checks and generate a violation report.

    Executes a set of QC queries (default or custom ``profile``) and
    reports violations at three severity levels: ERROR, WARN, INFO.
    Use ``fail_on`` to set the threshold (e.g. ``"ERROR"`` or ``"WARN"``).
    """
    args = build_global_args(
        catalog=catalog, prefixes=prefixes, add_prefix=add_prefix,
        noprefixes=noprefixes, verbose=verbose, strict=strict,
        xml_entities=xml_entities,
    )
    args.append("report")
    if input:
        args.extend(["--input", input])
    if fail_on:
        args.extend(["--fail-on", fail_on])
    if labels is not None:
        args.extend(["--labels", str(labels).lower()])
    if profile:
        args.extend(["--profile", profile])
    if limit is not None:
        args.extend(["--limit", str(limit)])
    if base_iri:
        args.extend(["--base-iri", base_iri])
    if tdb is not None:
        args.extend(["--tdb", str(tdb).lower()])
    if format:
        args.extend(["--format", format])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
