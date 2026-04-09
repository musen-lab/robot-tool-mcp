"""ROBOT reduce command — remove redundant subClassOf axioms."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_reduce(
    input: str | None = None,
    output: str | None = None,
    reasoner: str = "ELK",
    preserve_annotated_axioms: bool | None = None,
    named_classes_only: bool | None = None,
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
    """Remove redundant subClassOf axioms using a reasoner.

    After reasoning, some asserted subclass relationships become redundant
    because they can be inferred through other paths.  This command strips
    those redundancies to keep the ontology minimal.
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
    args.append("reduce")
    if input:
        args.extend(["--input", input])
    args.extend(["--reasoner", reasoner])
    if preserve_annotated_axioms is not None:
        args.extend(
            ["--preserve-annotated-axioms", str(preserve_annotated_axioms).lower()]
        )
    if named_classes_only is not None:
        args.extend(["--named-classes-only", str(named_classes_only).lower()])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
