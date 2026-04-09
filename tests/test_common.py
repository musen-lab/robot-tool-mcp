"""Tests for shared argument building helpers."""

from robot_mcp.commands._common import build_global_args, ensure_list


class TestBuildGlobalArgs:
    """Tests for build_global_args."""

    def test_empty_defaults(self) -> None:
        """Returns empty list when no options are set."""
        assert build_global_args() == []

    def test_catalog(self) -> None:
        """Adds --catalog flag."""
        result = build_global_args(catalog="catalog.xml")
        assert result == ["--catalog", "catalog.xml"]

    def test_prefixes(self) -> None:
        """Adds --prefixes flag."""
        result = build_global_args(prefixes="prefixes.json")
        assert result == ["--prefixes", "prefixes.json"]

    def test_add_prefix_single(self) -> None:
        """Adds a single --add-prefix flag."""
        result = build_global_args(add_prefix=["ex: http://example.org/"])
        assert result == ["--add-prefix", "ex: http://example.org/"]

    def test_add_prefix_multiple(self) -> None:
        """Repeats --add-prefix for each entry."""
        result = build_global_args(
            add_prefix=["ex: http://example.org/", "foo: http://foo.bar/"]
        )
        assert result == [
            "--add-prefix",
            "ex: http://example.org/",
            "--add-prefix",
            "foo: http://foo.bar/",
        ]

    def test_noprefixes(self) -> None:
        """Adds --noprefixes boolean flag."""
        result = build_global_args(noprefixes=True)
        assert result == ["--noprefixes"]

    def test_verbose(self) -> None:
        """Adds --verbose boolean flag."""
        result = build_global_args(verbose=True)
        assert result == ["--verbose"]

    def test_strict(self) -> None:
        """Adds --strict boolean flag."""
        result = build_global_args(strict=True)
        assert result == ["--strict"]

    def test_xml_entities(self) -> None:
        """Adds --xml-entities boolean flag."""
        result = build_global_args(xml_entities=True)
        assert result == ["--xml-entities"]

    def test_multiple_options(self) -> None:
        """Combines multiple options in correct order."""
        result = build_global_args(
            catalog="catalog.xml",
            verbose=True,
            strict=True,
        )
        assert result == ["--catalog", "catalog.xml", "--verbose", "--strict"]

    def test_false_booleans_omitted(self) -> None:
        """False booleans produce no flags."""
        result = build_global_args(
            noprefixes=False, verbose=False, strict=False, xml_entities=False
        )
        assert result == []

    def test_add_prefix_string_normalized(self) -> None:
        """A single string for add_prefix is normalized to a list."""
        result = build_global_args(add_prefix="ex: http://example.org/")
        assert result == ["--add-prefix", "ex: http://example.org/"]


class TestEnsureList:
    """Tests for ensure_list string-to-list normalization."""

    def test_none_returns_none(self) -> None:
        """None stays None."""
        assert ensure_list(None) is None

    def test_string_becomes_single_element_list(self) -> None:
        """A bare string is wrapped in a list."""
        assert ensure_list("hello") == ["hello"]

    def test_list_unchanged(self) -> None:
        """A list passes through unchanged."""
        assert ensure_list(["a", "b"]) == ["a", "b"]

    def test_empty_list_unchanged(self) -> None:
        """An empty list passes through unchanged."""
        assert ensure_list([]) == []

    def test_empty_string_becomes_list(self) -> None:
        """An empty string becomes a single-element list."""
        assert ensure_list("") == [""]
