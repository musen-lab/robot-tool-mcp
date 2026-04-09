"""ROBOT query command — execute SPARQL queries against ontologies."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_query(
    input: str | None = None,
    output: str | None = None,
    query: list[str] | None = None,
    queries: list[str] | None = None,
    output_dir: str | None = None,
    update: list[str] | None = None,
    use_graphs: bool | None = None,
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
    """Execute SPARQL queries against an ontology.

    Use ``query`` for pairs of query-file and output-file (e.g.
    ``["cell_part.sparql", "results/cell_part.csv"]``).  Use ``queries``
    with ``output_dir`` for batch execution.  Use ``update`` for SPARQL
    UPDATE operations that modify the ontology.

    Query types: ASK (true/false), SELECT (tabular CSV), CONSTRUCT (RDF).
    Use ``tdb`` for large ontologies to use disk-backed storage.
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
    args.append("query")
    if input:
        args.extend(["--input", input])
    if query:
        for q in query:
            args.extend(["--query", q])
    if queries:
        for q in queries:
            args.extend(["--queries", q])
    if output_dir:
        args.extend(["--output-dir", output_dir])
    if update:
        for u in update:
            args.extend(["--update", u])
    if use_graphs is not None:
        args.extend(["--use-graphs", str(use_graphs).lower()])
    if tdb is not None:
        args.extend(["--tdb", str(tdb).lower()])
    if format:
        args.extend(["--format", format])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
