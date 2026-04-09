"""Tests for individual command tools — argument building."""

import asyncio
from unittest.mock import AsyncMock, patch

from robot_mcp.commands.merge import robot_merge
from robot_mcp.commands.annotate import robot_annotate
from robot_mcp.commands.convert import robot_convert
from robot_mcp.commands.reason import robot_reason
from robot_mcp.commands.extract import robot_extract
from robot_mcp.commands.filter import robot_filter
from robot_mcp.commands.remove import robot_remove
from robot_mcp.commands.query import robot_query
from robot_mcp.commands.diff import robot_diff
from robot_mcp.commands.report import robot_report
from robot_mcp.commands.measure import robot_measure
from robot_mcp.commands.template import robot_template
from robot_mcp.commands.export import robot_export
from robot_mcp.commands.collapse import robot_collapse
from robot_mcp.commands.rename import robot_rename
from robot_mcp.commands.validate_profile import robot_validate_profile


class TestMerge:
    """Tests for robot_merge argument building."""

    @patch("robot_mcp.commands.merge.run_robot", new_callable=AsyncMock)
    def test_basic_merge(self, mock_run: AsyncMock) -> None:
        """Single input and output."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_merge(input=["a.owl"], output="merged.owl"))
        args = mock_run.call_args[0][0]
        assert args == ["merge", "--input", "a.owl", "--output", "merged.owl"]

    @patch("robot_mcp.commands.merge.run_robot", new_callable=AsyncMock)
    def test_multiple_inputs(self, mock_run: AsyncMock) -> None:
        """Multiple inputs produce repeated --input flags."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_merge(input=["a.owl", "b.owl", "c.owl"]))
        args = mock_run.call_args[0][0]
        assert args.count("--input") == 3

    @patch("robot_mcp.commands.merge.run_robot", new_callable=AsyncMock)
    def test_collapse_import_closure(self, mock_run: AsyncMock) -> None:
        """Boolean option collapse_import_closure."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_merge(input=["a.owl"], collapse_import_closure=True))
        args = mock_run.call_args[0][0]
        assert "--collapse-import-closure" in args
        idx = args.index("--collapse-import-closure")
        assert args[idx + 1] == "true"

    @patch("robot_mcp.commands.merge.run_robot", new_callable=AsyncMock)
    def test_extra_args(self, mock_run: AsyncMock) -> None:
        """Extra args are appended."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_merge(
                input=["a.owl"],
                extra_args=["--include-annotations", "true"],
            )
        )
        args = mock_run.call_args[0][0]
        assert "--include-annotations" in args
        assert "true" in args

    @patch("robot_mcp.commands.merge.run_robot", new_callable=AsyncMock)
    def test_global_options(self, mock_run: AsyncMock) -> None:
        """Global options precede the merge command."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_merge(
                input=["a.owl"],
                catalog="catalog.xml",
                verbose=True,
            )
        )
        args = mock_run.call_args[0][0]
        merge_idx = args.index("merge")
        catalog_idx = args.index("--catalog")
        verbose_idx = args.index("--verbose")
        assert catalog_idx < merge_idx
        assert verbose_idx < merge_idx


class TestAnnotate:
    """Tests for robot_annotate argument building."""

    @patch("robot_mcp.commands.annotate.run_robot", new_callable=AsyncMock)
    def test_ontology_and_version_iri(self, mock_run: AsyncMock) -> None:
        """Sets ontology and version IRI."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_annotate(
                input="edit.owl",
                ontology_iri="https://example.org/ont",
                version_iri="https://example.org/ont/v1",
                output="annotated.owl",
            )
        )
        args = mock_run.call_args[0][0]
        assert "--ontology-iri" in args
        assert "--version-iri" in args
        assert "https://example.org/ont" in args

    @patch("robot_mcp.commands.annotate.run_robot", new_callable=AsyncMock)
    def test_multiple_annotations(self, mock_run: AsyncMock) -> None:
        """Multiple annotations produce repeated flags."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_annotate(
                input="edit.owl",
                annotation=["rdfs:comment 'Test'", "rdfs:label 'My Ontology'"],
            )
        )
        args = mock_run.call_args[0][0]
        assert args.count("--annotation") == 2

    @patch("robot_mcp.commands.annotate.run_robot", new_callable=AsyncMock)
    def test_remove_annotations(self, mock_run: AsyncMock) -> None:
        """Remove annotations flag is a bare flag."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_annotate(input="edit.owl", remove_annotations=True))
        args = mock_run.call_args[0][0]
        assert "--remove-annotations" in args


class TestConvert:
    """Tests for robot_convert argument building."""

    @patch("robot_mcp.commands.convert.run_robot", new_callable=AsyncMock)
    def test_format_flag(self, mock_run: AsyncMock) -> None:
        """Explicit format flag."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_convert(input="a.owl", format="obo", output="a.obo"))
        args = mock_run.call_args[0][0]
        assert args == [
            "convert",
            "--input",
            "a.owl",
            "--format",
            "obo",
            "--output",
            "a.obo",
        ]

    @patch("robot_mcp.commands.convert.run_robot", new_callable=AsyncMock)
    def test_check_flag(self, mock_run: AsyncMock) -> None:
        """Check flag as boolean."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_convert(input="a.owl", check=False))
        args = mock_run.call_args[0][0]
        assert "--check" in args
        idx = args.index("--check")
        assert args[idx + 1] == "false"


class TestReason:
    """Tests for robot_reason argument building."""

    @patch("robot_mcp.commands.reason.run_robot", new_callable=AsyncMock)
    def test_default_reasoner(self, mock_run: AsyncMock) -> None:
        """Default reasoner is ELK."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_reason(input="a.owl"))
        args = mock_run.call_args[0][0]
        assert "--reasoner" in args
        idx = args.index("--reasoner")
        assert args[idx + 1] == "ELK"

    @patch("robot_mcp.commands.reason.run_robot", new_callable=AsyncMock)
    def test_custom_reasoner(self, mock_run: AsyncMock) -> None:
        """Custom reasoner selection."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_reason(input="a.owl", reasoner="HermiT"))
        args = mock_run.call_args[0][0]
        idx = args.index("--reasoner")
        assert args[idx + 1] == "HermiT"

    @patch("robot_mcp.commands.reason.run_robot", new_callable=AsyncMock)
    def test_axiom_generators(self, mock_run: AsyncMock) -> None:
        """Axiom generators string."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_reason(
                input="a.owl",
                axiom_generators="SubClass EquivalentClass",
            )
        )
        args = mock_run.call_args[0][0]
        assert "--axiom-generators" in args
        assert "SubClass EquivalentClass" in args


class TestExtract:
    """Tests for robot_extract argument building."""

    @patch("robot_mcp.commands.extract.run_robot", new_callable=AsyncMock)
    def test_method_and_terms(self, mock_run: AsyncMock) -> None:
        """Extraction method with term list."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_extract(
                input="ont.owl",
                method="BOT",
                term=["GO:0005634", "GO:0005737"],
                output="module.owl",
            )
        )
        args = mock_run.call_args[0][0]
        assert "--method" in args
        idx = args.index("--method")
        assert args[idx + 1] == "BOT"
        assert args.count("--term") == 2


class TestFilter:
    """Tests for robot_filter argument building."""

    @patch("robot_mcp.commands.filter.run_robot", new_callable=AsyncMock)
    def test_select_flags(self, mock_run: AsyncMock) -> None:
        """Multiple select values."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_filter(
                input="ont.owl",
                term=["UBERON:0000062"],
                select=["annotations", "self", "descendants"],
            )
        )
        args = mock_run.call_args[0][0]
        assert args.count("--select") == 3


class TestRemove:
    """Tests for robot_remove argument building."""

    @patch("robot_mcp.commands.remove.run_robot", new_callable=AsyncMock)
    def test_trim_and_preserve(self, mock_run: AsyncMock) -> None:
        """Trim and preserve-structure booleans."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_remove(
                input="ont.owl",
                term=["X:001"],
                trim=True,
                preserve_structure=False,
            )
        )
        args = mock_run.call_args[0][0]
        assert "--trim" in args
        assert "--preserve-structure" in args
        idx = args.index("--trim")
        assert args[idx + 1] == "true"
        idx = args.index("--preserve-structure")
        assert args[idx + 1] == "false"


class TestQuery:
    """Tests for robot_query argument building."""

    @patch("robot_mcp.commands.query.run_robot", new_callable=AsyncMock)
    def test_query_pairs(self, mock_run: AsyncMock) -> None:
        """Query file and output pairs."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_query(
                input="ont.owl",
                query=["q.sparql", "results.csv"],
            )
        )
        args = mock_run.call_args[0][0]
        assert args.count("--query") == 2

    @patch("robot_mcp.commands.query.run_robot", new_callable=AsyncMock)
    def test_update_flag(self, mock_run: AsyncMock) -> None:
        """SPARQL UPDATE via --update."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_query(
                input="ont.owl",
                update=["update.ru"],
                output="updated.owl",
            )
        )
        args = mock_run.call_args[0][0]
        assert "--update" in args


class TestDiff:
    """Tests for robot_diff argument building."""

    @patch("robot_mcp.commands.diff.run_robot", new_callable=AsyncMock)
    def test_left_right(self, mock_run: AsyncMock) -> None:
        """Uses --left and --right instead of --input."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_diff(left="a.owl", right="b.owl"))
        args = mock_run.call_args[0][0]
        assert "--left" in args
        assert "--right" in args
        assert "--input" not in args

    @patch("robot_mcp.commands.diff.run_robot", new_callable=AsyncMock)
    def test_format_and_labels(self, mock_run: AsyncMock) -> None:
        """Format and labels flags."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_diff(left="a.owl", right="b.owl", format="markdown", labels=True)
        )
        args = mock_run.call_args[0][0]
        assert "--format" in args
        assert "markdown" in args
        assert "--labels" in args


class TestReport:
    """Tests for robot_report argument building."""

    @patch("robot_mcp.commands.report.run_robot", new_callable=AsyncMock)
    def test_fail_on_and_profile(self, mock_run: AsyncMock) -> None:
        """Fail-on threshold and custom profile."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_report(
                input="ont.owl",
                fail_on="WARN",
                profile="custom.txt",
            )
        )
        args = mock_run.call_args[0][0]
        assert "--fail-on" in args
        assert "WARN" in args
        assert "--profile" in args


class TestMeasure:
    """Tests for robot_measure argument building."""

    @patch("robot_mcp.commands.measure.run_robot", new_callable=AsyncMock)
    def test_default_metrics(self, mock_run: AsyncMock) -> None:
        """Default metrics is 'essential'."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_measure(input="ont.owl"))
        args = mock_run.call_args[0][0]
        idx = args.index("--metrics")
        assert args[idx + 1] == "essential"

    @patch("robot_mcp.commands.measure.run_robot", new_callable=AsyncMock)
    def test_custom_format(self, mock_run: AsyncMock) -> None:
        """Custom output format."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_measure(input="ont.owl", metrics="extended", format="json"))
        args = mock_run.call_args[0][0]
        assert "extended" in args
        assert "--format" in args
        assert "json" in args


class TestTemplate:
    """Tests for robot_template argument building."""

    @patch("robot_mcp.commands.template.run_robot", new_callable=AsyncMock)
    def test_template_with_prefix(self, mock_run: AsyncMock) -> None:
        """Template file and custom prefix."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_template(
                template=["terms.csv"],
                prefix=["ex: http://example.org/"],
                ontology_iri="https://example.org/ont",
                output="result.owl",
            )
        )
        args = mock_run.call_args[0][0]
        assert "--template" in args
        assert "--prefix" in args
        assert "--ontology-iri" in args


class TestExport:
    """Tests for robot_export argument building."""

    @patch("robot_mcp.commands.export.run_robot", new_callable=AsyncMock)
    def test_header_and_export(self, mock_run: AsyncMock) -> None:
        """Header and export path."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_export(
                input="ont.owl",
                header="ID|LABEL",
                export="output.csv",
            )
        )
        args = mock_run.call_args[0][0]
        assert "--header" in args
        assert "ID|LABEL" in args
        assert "--export" in args


class TestCollapse:
    """Tests for robot_collapse argument building."""

    @patch("robot_mcp.commands.collapse.run_robot", new_callable=AsyncMock)
    def test_threshold_and_precious(self, mock_run: AsyncMock) -> None:
        """Threshold as int and precious terms."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_collapse(
                input="ont.owl",
                threshold=3,
                precious=["UBERON:0000483"],
            )
        )
        args = mock_run.call_args[0][0]
        assert "--threshold" in args
        assert "3" in args
        assert "--precious" in args


class TestRename:
    """Tests for robot_rename argument building."""

    @patch("robot_mcp.commands.rename.run_robot", new_callable=AsyncMock)
    def test_mapping(self, mock_run: AsyncMock) -> None:
        """Individual IRI mapping."""
        mock_run.return_value = {"success": True}
        asyncio.run(
            robot_rename(
                input="ont.owl",
                mapping=["obo:BFO_0000051 ex:partOf"],
            )
        )
        args = mock_run.call_args[0][0]
        assert "--mapping" in args
        assert "obo:BFO_0000051 ex:partOf" in args


class TestValidateProfile:
    """Tests for robot_validate_profile argument building."""

    @patch("robot_mcp.commands.validate_profile.run_robot", new_callable=AsyncMock)
    def test_default_profile(self, mock_run: AsyncMock) -> None:
        """Default profile is DL."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_validate_profile(input="ont.owl"))
        args = mock_run.call_args[0][0]
        idx = args.index("--profile")
        assert args[idx + 1] == "DL"

    @patch("robot_mcp.commands.validate_profile.run_robot", new_callable=AsyncMock)
    def test_custom_profile(self, mock_run: AsyncMock) -> None:
        """Custom OWL 2 profile."""
        mock_run.return_value = {"success": True}
        asyncio.run(robot_validate_profile(input="ont.owl", profile="EL"))
        args = mock_run.call_args[0][0]
        idx = args.index("--profile")
        assert args[idx + 1] == "EL"
