"""ROBOT repair command — fix common ontology problems."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import StrOrList, build_global_args, ensure_list


async def robot_repair(
    input: str | None = None,
    output: str | None = None,
    invalid_references: bool | None = None,
    annotation_property: StrOrList = None,
    merge_axiom_annotations: bool | None = None,
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
    """Fix common ontology problems.

    Repairs include: updating references to deprecated classes (replacing
    them with their replacements), merging duplicate axiom annotations,
    and fixing invalid references.
    """
    annotation_property = ensure_list(annotation_property)
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
    args.append("repair")
    if input:
        args.extend(["--input", input])
    if invalid_references is not None:
        args.extend(["--invalid-references", str(invalid_references).lower()])
    if annotation_property:
        for a in annotation_property:
            args.extend(["--annotation-property", a])
    if merge_axiom_annotations is not None:
        args.extend(["--merge-axiom-annotations", str(merge_axiom_annotations).lower()])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
