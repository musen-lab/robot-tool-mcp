"""ROBOT validate-profile command — check OWL 2 profile conformance."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import StrOrList, build_global_args, ensure_list


async def robot_validate_profile(
    input: str | None = None,
    output: str | None = None,
    profile: str = "DL",
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
    """Check ontology conformance to an OWL 2 profile.

    Profiles: EL, RL, QL, DL, Full.  The output contains any violations
    found.  ROBOT exits with non-zero code if the ontology does not
    conform to the specified profile.
    """
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
    args.append("validate-profile")
    if input:
        args.extend(["--input", input])
    args.extend(["--profile", profile])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
