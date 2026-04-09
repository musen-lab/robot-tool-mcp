"""ROBOT annotate command — add metadata to an ontology."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_annotate(
    input: str | None = None,
    output: str | None = None,
    ontology_iri: str | None = None,
    version_iri: str | None = None,
    annotation: list[str] | None = None,
    link_annotation: list[str] | None = None,
    language_annotation: list[str] | None = None,
    typed_annotation: list[str] | None = None,
    annotation_file: str | None = None,
    remove_annotations: bool = False,
    annotate_derived_from: bool | None = None,
    annotate_defined_by: bool | None = None,
    working_directory: str | None = None,
    catalog: str | None = None,
    prefixes: str | None = None,
    add_prefix: list[str] | None = None,
    noprefixes: bool = False,
    verbose: bool = False,
    strict: bool = False,
    xml_entities: bool = False,
    extra_args: list[str] | None = None,  # use ["--help"] to list available flags
) -> dict[str, Any]:
    """Add metadata annotations to an ontology.

    Set the ontology IRI, version IRI, and add annotation properties.
    Each ``annotation`` value is a string like
    ``"rdfs:comment 'Example ontology'"``.  Use ``link_annotation`` for
    IRI-valued annotations and ``language_annotation`` for language-tagged
    literals.
    """
    args = build_global_args(
        catalog=catalog, prefixes=prefixes, add_prefix=add_prefix,
        noprefixes=noprefixes, verbose=verbose, strict=strict,
        xml_entities=xml_entities,
    )
    args.append("annotate")
    if input:
        args.extend(["--input", input])
    if ontology_iri:
        args.extend(["--ontology-iri", ontology_iri])
    if version_iri:
        args.extend(["--version-iri", version_iri])
    if annotation:
        for a in annotation:
            args.extend(["--annotation", a])
    if link_annotation:
        for a in link_annotation:
            args.extend(["--link-annotation", a])
    if language_annotation:
        for a in language_annotation:
            args.extend(["--language-annotation", a])
    if typed_annotation:
        for a in typed_annotation:
            args.extend(["--typed-annotation", a])
    if annotation_file:
        args.extend(["--annotation-file", annotation_file])
    if remove_annotations:
        args.append("--remove-annotations")
    if annotate_derived_from is not None:
        args.extend(["--annotate-derived-from", str(annotate_derived_from).lower()])
    if annotate_defined_by is not None:
        args.extend(["--annotate-defined-by", str(annotate_defined_by).lower()])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
