"""ROBOT verify command — check ontology against SPARQL rules."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import StrOrList, build_global_args, ensure_list


async def robot_verify(
    input: str | None = None,
    queries: StrOrList = None,
    output_dir: str | None = None,
    fail_on_violation: bool | None = None,
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
    """Check an ontology for rule violations using SPARQL SELECT queries.

    Each query file should contain a SPARQL SELECT.  If the query returns
    any results, those are violations.  ROBOT exits with a non-zero code
    when violations are found (controllable via ``fail_on_violation``).
    """
    queries = ensure_list(queries)
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
    args.append("verify")
    if input:
        args.extend(["--input", input])
    if queries:
        for q in queries:
            args.extend(["--queries", q])
    if output_dir:
        args.extend(["--output-dir", output_dir])
    if fail_on_violation is not None:
        args.extend(["--fail-on-violation", str(fail_on_violation).lower()])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
