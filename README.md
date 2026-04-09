# robot-mcp

MCP server wrapping the [ROBOT](https://robot.obolibrary.org/) command-line tool for OWL ontology editing.

## Prerequisites

ROBOT must be installed and available on your `PATH`:

```bash
robot --version
```

See [ROBOT installation](https://robot.obolibrary.org/) for setup instructions.

## Installation

### With uvx (recommended)

```bash
uvx --from git+https://github.com/<owner>/robot-mcp robot-mcp
```

### From source

```bash
git clone https://github.com/<owner>/robot-mcp.git
cd robot-mcp
uv run robot-mcp
```

## Claude Desktop Configuration

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "robot-mcp": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/<owner>/robot-mcp", "robot-mcp"]
    }
  }
}
```

Or for local development:

```json
{
  "mcpServers": {
    "robot-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/robot-mcp", "robot-mcp"]
    }
  }
}
```

## Tools

### Individual Command Tools (25 tools)

Each ROBOT command is exposed as a dedicated MCP tool with typed parameters:

| Tool | Description |
|------|-------------|
| `robot_annotate` | Add metadata annotations to an ontology |
| `robot_collapse` | Simplify class hierarchies by removing intermediates |
| `robot_convert` | Transform ontology between formats (OWL, OBO, TTL, etc.) |
| `robot_diff` | Compare two ontologies semantically |
| `robot_expand` | Convert shortcut annotations into OWL axioms |
| `robot_explain` | Debug inferred statements with minimal explanations |
| `robot_export` | Generate tabular output (CSV, TSV, JSON, HTML, XLSX) |
| `robot_extract` | Create a subset module (STAR, BOT, TOP, MIREOT) |
| `robot_filter` | Selectively copy axioms (inverse of remove) |
| `robot_materialize` | Assert inferred superclass relationships |
| `robot_measure` | Compute ontology metrics and statistics |
| `robot_merge` | Combine multiple ontologies into one |
| `robot_mirror` | Cache imported ontologies locally |
| `robot_query` | Execute SPARQL queries (SELECT, ASK, CONSTRUCT, UPDATE) |
| `robot_reason` | Run OWL reasoner (ELK, HermiT, JFact, Whelk) |
| `robot_reduce` | Remove redundant subClassOf axioms |
| `robot_relax` | Convert equivalence axioms to subclass axioms |
| `robot_remove` | Eliminate selected axioms (inverse of filter) |
| `robot_rename` | Modify entity IRIs |
| `robot_repair` | Fix common ontology problems |
| `robot_report` | Run quality control checks with violation report |
| `robot_template` | Convert tabular data (CSV/TSV) into OWL |
| `robot_unmerge` | Remove axioms of one ontology from another |
| `robot_validate_profile` | Check OWL 2 profile conformance (EL/RL/QL/DL) |
| `robot_verify` | Check ontology against SPARQL rules |

### Chain Tool

The `robot_chain` tool pipelines multiple commands in a single ROBOT process. Ontology objects pass **in-memory** between steps — no intermediate files needed.

```json
{
  "steps": [
    {"command": "merge", "input": ["edit.owl", "base.owl"]},
    {"command": "reason", "reasoner": "ELK"},
    {"command": "annotate", "ontology_iri": "https://example.org/my.owl"},
    {"command": "convert", "format": "ofn", "output": "result.owl"}
  ]
}
```

This produces a single CLI call:
```
robot merge --input edit.owl --input base.owl \
      reason --reasoner ELK \
      annotate --ontology-iri https://example.org/my.owl \
      convert --format ofn --output result.owl
```

**Argument mapping rules:**
- Underscores become hyphens: `ontology_iri` → `--ontology-iri`
- Lists repeat the flag: `{"input": ["a.owl", "b.owl"]}` → `--input a.owl --input b.owl`
- Booleans become strings: `true` → `"true"`

### Common Workflows

**Build a release:**
```json
{
  "steps": [
    {"command": "merge", "input": ["edit.owl"]},
    {"command": "reason", "reasoner": "ELK"},
    {"command": "relax"},
    {"command": "reduce", "reasoner": "ELK"},
    {"command": "annotate", "ontology_iri": "https://example.org/release.owl",
     "version_iri": "https://example.org/2024-01-01/release.owl"},
    {"command": "convert", "output": "release.owl"}
  ]
}
```

**Extract a module:**
```json
{
  "steps": [
    {"command": "merge", "input": ["full-ontology.owl"]},
    {"command": "extract", "method": "BOT", "term": ["GO:0005634", "GO:0005737"]},
    {"command": "annotate", "ontology_iri": "https://example.org/module.owl"},
    {"command": "convert", "output": "module.owl"}
  ]
}
```

**Quality check:**
```json
{
  "steps": [
    {"command": "merge", "input": ["edit.owl"]},
    {"command": "report", "fail_on": "ERROR", "output": "report.tsv"}
  ]
}
```

## Global Options

All tools support these global options:

| Option | Description |
|--------|-------------|
| `catalog` | XML catalog file for resolving imports |
| `prefixes` | JSON-LD prefix file |
| `add_prefix` | Add individual prefixes (list) |
| `noprefixes` | Disable default prefixes |
| `verbose` | Enable verbose logging |
| `strict` | Fail on unparsed triples |
| `xml_entities` | Use XML entities in RDF/XML output |
| `working_directory` | Working directory for file paths |
| `extra_args` | Escape hatch for rarely-used flags (list of strings) |

## How to Contribute

1. Fork the repository
2. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Install dev dependencies:
   ```bash
   uv sync --dev
   ```
4. Make your changes and ensure code quality:
   ```bash
   uv run ruff format src/
   uv run ruff check src/
   ```
5. Commit your changes and push to your fork
6. Open a Pull Request against `main`

The `main` branch is protected — all changes must go through a PR.

## License

BSD 2-Clause License
