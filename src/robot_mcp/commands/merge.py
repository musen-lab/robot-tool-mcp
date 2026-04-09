"""ROBOT merge command — combine multiple ontologies into one."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import StrOrList, build_global_args, ensure_list


async def robot_merge(
    input: StrOrList = None,
    input_iri: StrOrList = None,
    inputs: str | None = None,
    output: str | None = None,
    collapse_import_closure: bool | None = None,
    include_annotations: bool | None = None,
    annotate_derived_from: bool | None = None,
    annotate_defined_by: bool | None = None,
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
    """Merge one or more OWL ontology files into a single ontology.

    Combine multiple ontology files.  Each ``input`` path or ``input_iri``
    IRI is loaded and merged.  Use ``inputs`` for glob patterns like
    ``"edit*.owl"``.  By default, import closures are merged and
    ``owl:imports`` statements are removed.
    """
    input = ensure_list(input)
    input_iri = ensure_list(input_iri)
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
    args.append("merge")
    if input:
        for i in input:
            args.extend(["--input", i])
    if input_iri:
        for i in input_iri:
            args.extend(["--input-iri", i])
    if inputs:
        args.extend(["--inputs", inputs])
    if collapse_import_closure is not None:
        args.extend(["--collapse-import-closure", str(collapse_import_closure).lower()])
    if include_annotations is not None:
        args.extend(["--include-annotations", str(include_annotations).lower()])
    if annotate_derived_from is not None:
        args.extend(["--annotate-derived-from", str(annotate_derived_from).lower()])
    if annotate_defined_by is not None:
        args.extend(["--annotate-defined-by", str(annotate_defined_by).lower()])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
