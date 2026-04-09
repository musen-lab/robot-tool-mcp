"""ROBOT expand command — convert shortcut annotations into axioms."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import StrOrList, build_global_args, ensure_list


async def robot_expand(
    input: str | None = None,
    output: str | None = None,
    expand_term: StrOrList = None,
    no_expand_term: StrOrList = None,
    annotate_expansion_axioms: bool | None = None,
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
    """Expand shortcut annotation properties (macros) into OWL axioms.

    Use ``expand_term`` to specify which macro properties to expand.
    Use ``no_expand_term`` to exclude specific properties.  Set
    ``annotate_expansion_axioms`` to mark generated axioms.
    """
    expand_term = ensure_list(expand_term)
    no_expand_term = ensure_list(no_expand_term)
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
    args.append("expand")
    if input:
        args.extend(["--input", input])
    if expand_term:
        for t in expand_term:
            args.extend(["--expand-term", t])
    if no_expand_term:
        for t in no_expand_term:
            args.extend(["--no-expand-term", t])
    if annotate_expansion_axioms is not None:
        args.extend(
            ["--annotate-expansion-axioms", str(annotate_expansion_axioms).lower()]
        )
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
