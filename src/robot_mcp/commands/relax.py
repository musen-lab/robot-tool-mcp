"""ROBOT relax command — convert equivalence axioms to subclass axioms."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_relax(
    input: str | None = None,
    output: str | None = None,
    exclude_named_classes: bool | None = None,
    include_subclass_of: bool | None = None,
    enforce_obo_format: bool | None = None,
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
    """Relax equivalence axioms into weaker subclass axioms.

    Converts EquivalentClasses axioms to SubClassOf axioms, making the
    ontology less restrictive while preserving the subclass hierarchy.
    Commonly used before ``reduce`` in pipelines like
    ``reason → relax → reduce``.
    """
    args = build_global_args(
        catalog=catalog, prefixes=prefixes, add_prefix=add_prefix,
        noprefixes=noprefixes, verbose=verbose, strict=strict,
        xml_entities=xml_entities,
    )
    args.append("relax")
    if input:
        args.extend(["--input", input])
    if exclude_named_classes is not None:
        args.extend(["--exclude-named-classes", str(exclude_named_classes).lower()])
    if include_subclass_of is not None:
        args.extend(["--include-subclass-of", str(include_subclass_of).lower()])
    if enforce_obo_format is not None:
        args.extend(["--enforce-obo-format", str(enforce_obo_format).lower()])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
