"""ROBOT extract command — create a subset module from a larger ontology."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_extract(
    input: str | None = None,
    output: str | None = None,
    method: str = "STAR",
    term: list[str] | None = None,
    term_file: str | None = None,
    upper_term: list[str] | None = None,
    lower_term: list[str] | None = None,
    branch_from_term: list[str] | None = None,
    imports: str | None = None,
    individuals: str | None = None,
    intermediates: str | None = None,
    copy_ontology_annotations: bool | None = None,
    annotate_with_source: bool | None = None,
    sources: str | None = None,
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
    """Extract a subset module from a larger ontology.

    Methods:
      - STAR: minimal module with seed terms and direct relationships
      - BOT: seed terms plus all superclasses
      - TOP: seed terms plus all subclasses
      - MIREOT: hierarchy-preserving extraction with upper/lower boundaries
      - subset: seed terms with materialized existential relationships

    Specify seed terms via ``term`` (list of CURIEs/IRIs) or ``term_file``.
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
    args.append("extract")
    if input:
        args.extend(["--input", input])
    args.extend(["--method", method])
    if term:
        for t in term:
            args.extend(["--term", t])
    if term_file:
        args.extend(["--term-file", term_file])
    if upper_term:
        for t in upper_term:
            args.extend(["--upper-term", t])
    if lower_term:
        for t in lower_term:
            args.extend(["--lower-term", t])
    if branch_from_term:
        for t in branch_from_term:
            args.extend(["--branch-from-term", t])
    if imports:
        args.extend(["--imports", imports])
    if individuals:
        args.extend(["--individuals", individuals])
    if intermediates:
        args.extend(["--intermediates", intermediates])
    if copy_ontology_annotations is not None:
        args.extend(
            ["--copy-ontology-annotations", str(copy_ontology_annotations).lower()]
        )
    if annotate_with_source is not None:
        args.extend(["--annotate-with-source", str(annotate_with_source).lower()])
    if sources:
        args.extend(["--sources", sources])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
