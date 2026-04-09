"""ROBOT rename command — modify entity IRIs."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_rename(
    input: str | None = None,
    output: str | None = None,
    mapping: list[str] | None = None,
    mappings: str | None = None,
    prefix_mappings: str | None = None,
    allow_missing_entities: bool | None = None,
    allow_duplicates: bool | None = None,
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
    """Rename entity IRIs via full replacement or prefix-based renaming.

    Use ``mapping`` for individual IRI replacements (e.g.
    ``"obo:BFO_0000051 ex:partOf"``).  Use ``mappings`` to point to a
    TSV file of old→new mappings.  Use ``prefix_mappings`` for bulk
    prefix replacement.
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
    args.append("rename")
    if input:
        args.extend(["--input", input])
    if mapping:
        for m in mapping:
            args.extend(["--mapping", m])
    if mappings:
        args.extend(["--mappings", mappings])
    if prefix_mappings:
        args.extend(["--prefix-mappings", prefix_mappings])
    if allow_missing_entities is not None:
        args.extend(["--allow-missing-entities", str(allow_missing_entities).lower()])
    if allow_duplicates is not None:
        args.extend(["--allow-duplicates", str(allow_duplicates).lower()])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
