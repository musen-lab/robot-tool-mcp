"""ROBOT explain command — compute explanations for inferred statements."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import build_global_args


async def robot_explain(
    input: str | None = None,
    reasoner: str = "ELK",
    axiom: str | None = None,
    explanation: str | None = None,
    mode: str | None = None,
    max: int | None = None,
    unsatisfiable: str | None = None,
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
    """Compute minimal axiom explanations for inferred statements.

    Useful for debugging classification issues.  Modes:
    ``entailment`` (explain why an axiom is entailed),
    ``inconsistency`` (explain why the ontology is inconsistent),
    ``unsatisfiability`` (explain why a class is unsatisfiable).

    The ``axiom`` parameter takes a Manchester-syntax axiom string like
    ``"'uvular muscle' SubClassOf 'muscle organ'"``.
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
    args.append("explain")
    if input:
        args.extend(["--input", input])
    args.extend(["--reasoner", reasoner])
    if axiom:
        args.extend(["--axiom", axiom])
    if explanation:
        args.extend(["--explanation", explanation])
    if mode:
        args.extend(["--mode", mode])
    if max is not None:
        args.extend(["--max", str(max)])
    if unsatisfiable:
        args.extend(["--unsatisfiable", unsatisfiable])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
