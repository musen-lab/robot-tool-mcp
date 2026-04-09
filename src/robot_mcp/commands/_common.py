"""Shared helpers for building ROBOT CLI arguments."""

# Type alias for parameters that accept a single string or a list of strings.
# Some MCP clients send "value" instead of ["value"], so we accept both.
StrOrList = list[str] | str | None


def ensure_list(value: StrOrList) -> list[str] | None:
    """Normalize a string-or-list parameter to a list."""
    if value is None:
        return None
    if isinstance(value, str):
        return [value]
    return value


def build_global_args(
    *,
    catalog: str | None = None,
    prefixes: str | None = None,
    add_prefix: StrOrList = None,
    noprefixes: bool = False,
    verbose: bool = False,
    strict: bool = False,
    xml_entities: bool = False,
) -> list[str]:
    """Build the global option arguments that precede any ROBOT subcommand."""
    add_prefix = ensure_list(add_prefix)
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
