"""Shared helpers for building ROBOT CLI arguments."""


def build_global_args(
    *,
    catalog: str | None = None,
    prefixes: str | None = None,
    add_prefix: list[str] | None = None,
    noprefixes: bool = False,
    verbose: bool = False,
    strict: bool = False,
    xml_entities: bool = False,
) -> list[str]:
    """Build the global option arguments that precede any ROBOT subcommand."""
    args: list[str] = []
    if catalog:
        args.extend(["--catalog", catalog])
    if prefixes:
        args.extend(["--prefixes", prefixes])
    if add_prefix:
        for p in add_prefix:
            args.extend(["--add-prefix", p])
    if noprefixes:
        args.append("--noprefixes")
    if verbose:
        args.append("--verbose")
    if strict:
        args.append("--strict")
    if xml_entities:
        args.append("--xml-entities")
    return args
