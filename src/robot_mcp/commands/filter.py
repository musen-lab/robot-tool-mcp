"""ROBOT filter command — selectively copy axioms from an ontology."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import StrOrList, build_global_args, ensure_list


async def robot_filter(
    input: str | None = None,
    output: str | None = None,
    term: StrOrList = None,
    term_file: str | None = None,
    exclude_term: StrOrList = None,
    exclude_terms: str | None = None,
    select: StrOrList = None,
    axioms: str | None = None,
    signature: bool | None = None,
    trim: bool | None = None,
    preserve_structure: bool | None = None,
    drop_axiom_annotations: StrOrList = None,
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
    """Selectively copy axioms from an ontology (inverse of remove).

    Specify terms to include via ``term`` or ``term_file``.  Use
    ``select`` to control which related terms to include (e.g.
    ``"self parents descendants annotations"``).  The ``trim`` flag
    controls whether axioms require ALL or ANY objects in the target set.
    """
    term = ensure_list(term)
    exclude_term = ensure_list(exclude_term)
    select = ensure_list(select)
    drop_axiom_annotations = ensure_list(drop_axiom_annotations)
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
    args.append("filter")
    if input:
        args.extend(["--input", input])
    if term:
        for t in term:
            args.extend(["--term", t])
    if term_file:
        args.extend(["--term-file", term_file])
    if exclude_term:
        for t in exclude_term:
            args.extend(["--exclude-term", t])
    if exclude_terms:
        args.extend(["--exclude-terms", exclude_terms])
    if select:
        for s in select:
            args.extend(["--select", s])
    if axioms:
        args.extend(["--axioms", axioms])
    if signature is not None:
        args.extend(["--signature", str(signature).lower()])
    if trim is not None:
        args.extend(["--trim", str(trim).lower()])
    if preserve_structure is not None:
        args.extend(["--preserve-structure", str(preserve_structure).lower()])
    if drop_axiom_annotations:
        for d in drop_axiom_annotations:
            args.extend(["--drop-axiom-annotations", d])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
