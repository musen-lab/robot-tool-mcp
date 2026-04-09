"""ROBOT reason command — run a reasoner on an ontology."""

from typing import Any

from robot_mcp._runner import run_robot
from robot_mcp.commands._common import StrOrList, build_global_args, ensure_list


async def robot_reason(
    input: str | None = None,
    output: str | None = None,
    reasoner: str = "ELK",
    axiom_generators: str | None = None,
    create_new_ontology: bool | None = None,
    equivalent_classes_allowed: str | None = None,
    exclude_duplicate_axioms: bool | None = None,
    exclude_owl_thing: bool | None = None,
    exclude_tautologies: str | None = None,
    annotate_inferred_axioms: bool | None = None,
    remove_redundant_subclass_axioms: bool | None = None,
    dump_unsatisfiable: str | None = None,
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
    """Run an OWL reasoner to classify the ontology and check consistency.

    Reasoner choices: ELK (default, fast, OWL 2 EL), HermiT (full OWL 2
    DL), JFact, Whelk, EMR (Expression Materializing Reasoner), Structural.
    The ``axiom_generators`` flag controls which inferred axioms to assert
    (e.g. ``"SubClass EquivalentClass DisjointClasses"``).
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
    args.append("reason")
    if input:
        args.extend(["--input", input])
    args.extend(["--reasoner", reasoner])
    if axiom_generators:
        args.extend(["--axiom-generators", axiom_generators])
    if create_new_ontology is not None:
        args.extend(["--create-new-ontology", str(create_new_ontology).lower()])
    if equivalent_classes_allowed:
        args.extend(["--equivalent-classes-allowed", equivalent_classes_allowed])
    if exclude_duplicate_axioms is not None:
        args.extend(
            ["--exclude-duplicate-axioms", str(exclude_duplicate_axioms).lower()]
        )
    if exclude_owl_thing is not None:
        args.extend(["--exclude-owl-thing", str(exclude_owl_thing).lower()])
    if exclude_tautologies:
        args.extend(["--exclude-tautologies", exclude_tautologies])
    if annotate_inferred_axioms is not None:
        args.extend(
            ["--annotate-inferred-axioms", str(annotate_inferred_axioms).lower()]
        )
    if remove_redundant_subclass_axioms is not None:
        args.extend(
            [
                "--remove-redundant-subclass-axioms",
                str(remove_redundant_subclass_axioms).lower(),
            ]
        )
    if dump_unsatisfiable:
        args.extend(["--dump-unsatisfiable", dump_unsatisfiable])
    if output:
        args.extend(["--output", output])
    if extra_args:
        args.extend(extra_args)
    return await run_robot(args, cwd=working_directory)
