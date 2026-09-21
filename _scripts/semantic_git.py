#!/usr/bin/env python3
"""Canonical human/AI CLI for Semantic Git capabilities.

Public interface rules:
- current Semantic Repository is auto-detected from the working directory;
- --root is only an optional override for another Semantic Repository;
- --namespace selects the target Semantic Namespace;
- omitting --namespace means the root Semantic Namespace.

The older per-script CLIs are implementation details and are not the supported
public interface.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import build_publication as publication
import compile_semantic_context as compiled
import semantic_index as index
import validate_structure as structure


CAPABILITIES = [
    {"route": "semantic-git://validate/structure", "kind": "command", "cli": "validate"},
    {"route": "semantic-git://publication/build", "kind": "command", "cli": "publication build"},
    {"route": "semantic-git://publication/status", "kind": "command", "cli": "publication status"},
    {"route": "semantic-git://index/build", "kind": "command", "cli": "index build"},
    {"route": "semantic-git://index/validate", "kind": "command", "cli": "index validate"},
    {"route": "semantic-git://index/query", "kind": "command", "cli": "index query"},
    {"route": "semantic-git://compiled/build", "kind": "command", "cli": "compiled build"},
    {"route": "semantic-git://compiled/validate", "kind": "command", "cli": "compiled validate"},
    {"route": "semantic-git://compiled/publication", "kind": "command", "cli": "compiled publication"},
    {"route": "semantic-git://skills/extraction", "kind": "skill", "implementation": ".opencode/skills/semantic-extraction/SKILL.md"},
    {"route": "semantic-git://skills/reconstruction", "kind": "skill", "implementation": ".opencode/skills/semantic-reconstruction/SKILL.md"},
    {"route": "semantic-git://skills/conceptual-review", "kind": "skill", "implementation": ".opencode/skills/semantic-conceptual-review/SKILL.md"},
    {"route": "semantic-git://skills/mathematical-review", "kind": "skill", "implementation": ".opencode/skills/semantic-mathematical-review/SKILL.md"},
    {"route": "semantic-git://skills/memory", "kind": "skill", "implementation": ".opencode/skills/semantic-memory/SKILL.md"},
]


class CliError(RuntimeError):
    pass


def git_root(path: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise CliError(f"{path} is not inside a Git repository")
    return Path(result.stdout.strip()).resolve()


def repository_root(override: str | None) -> Path:
    if override is None:
        root = git_root(Path.cwd())
    else:
        requested = Path(override).expanduser().resolve()
        root = git_root(requested)
        if root != requested:
            raise CliError("--root must point to the Semantic Repository root, not to a subdirectory")
    if not (root / "SEMANTIC_GIT.md").is_file():
        raise CliError(f"SEMANTIC_GIT.md not found at Semantic Repository root: {root}")
    return root


def namespace_value(value: str | None) -> str:
    return "." if value in {None, "", "root"} else value


def namespace_dir(root: Path, value: str | None) -> Path:
    namespaces = index.namespaces(root)
    namespace = index.resolve_scope(root, namespace_value(value), namespaces)
    return namespace["path"]


def user_path(root: Path, value: str | None) -> Path | None:
    if value is None:
        return None
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def validate_repository(root: Path, spec: Path) -> None:
    validator = structure.Validator(root, spec)
    validator.run()
    if validator.result() == "FAIL":
        messages = [
            f"{finding['rule']}: {finding['path']}: {finding['message']}"
            for finding in validator.findings
        ]
        raise CliError("structure validation returned FAIL" + ("; " + "; ".join(messages) if messages else ""))


def publication_operation(root: Path, target: Path, spec: Path, args: argparse.Namespace) -> dict:
    """Run publication after repository-level validation.

    The legacy publication module validates its target directory as if it were
    the repository root. The canonical CLI deliberately bypasses that legacy
    wrapper after validating the actual Semantic Repository root.
    """
    validate_repository(root, spec)
    original_validator = publication.run_validator
    publication.run_validator = lambda *_args, **_kwargs: None
    try:
        if args.operation == "build":
            return publication.build(target, spec, args.pdf, args.theme)
        return publication.check_status(target, spec)
    finally:
        publication.run_validator = original_validator


def emit_capabilities(as_json: bool) -> int:
    if as_json:
        print(json.dumps({"scheme": "semantic-git://", "capabilities": CAPABILITIES}, ensure_ascii=False, indent=2))
        return 0
    print("semantic-git://")
    print("├── validate/structure")
    print("├── publication/{build,status}")
    print("├── index/{build,validate,query}")
    print("├── compiled/{build,validate,publication}")
    print("└── skills/{extraction,reconstruction,conceptual-review,mathematical-review,memory}")
    return 0


def add_namespace(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--namespace",
        default=".",
        help="target Semantic Namespace path; default: root Semantic Namespace",
    )


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="semantic-git",
        description="Canonical Semantic Git CLI. Repository is auto-detected; use --namespace for the target domain.",
    )
    p.add_argument(
        "--root",
        help="optional override of the Semantic Repository root; normally auto-detected from the current directory",
    )
    top = p.add_subparsers(dest="area", required=True)

    capabilities = top.add_parser("capabilities", help="list command and skill capability routes")
    capabilities.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    validate = top.add_parser("validate", help="validate the current Semantic Repository")
    validate.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    publication_group = top.add_parser("publication", help="publication capabilities")
    publication_commands = publication_group.add_subparsers(dest="operation", required=True)
    publication_build = publication_commands.add_parser("build", help="build namespace publication")
    add_namespace(publication_build)
    publication_build.add_argument("--pdf", action="store_true", help="also generate PUBLICATION.pdf")
    publication_build.add_argument("--theme", choices=tuple(publication.PDF_THEMES), default="blue", help="PDF theme; default: blue")
    publication_build.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    publication_status = publication_commands.add_parser("status", help="check publication freshness")
    add_namespace(publication_status)
    publication_status.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    index_group = top.add_parser("index", help="semantic index capabilities")
    index_commands = index_group.add_subparsers(dest="operation", required=True)
    index_build = index_commands.add_parser("build", help="build semantic index")
    add_namespace(index_build)
    index_validate = index_commands.add_parser("validate", help="validate semantic index")
    add_namespace(index_validate)
    index_query = index_commands.add_parser("query", help="query semantic index")
    add_namespace(index_query)
    index_query.add_argument("--id", dest="node_id", help="exact canonical node id")
    index_query.add_argument("--text", help="text search")
    index_query.add_argument("--type", choices=sorted(index.NODE_TYPES), help="node type")

    compiled_group = top.add_parser("compiled", help="Compiled Semantic Context capabilities")
    compiled_commands = compiled_group.add_subparsers(dest="operation", required=True)
    compiled_build = compiled_commands.add_parser("build", help="build compiled.ai.md")
    add_namespace(compiled_build)
    compiled_build.add_argument("--output", help="optional output path; default: <namespace>/compiled.ai.md")
    compiled_validate = compiled_commands.add_parser("validate", help="validate compiled.ai.md")
    add_namespace(compiled_validate)
    compiled_validate.add_argument("--compiled", help="optional compiled.ai.md path")
    compiled_publication = compiled_commands.add_parser("publication", help="project publication from compiled.ai.md")
    add_namespace(compiled_publication)
    compiled_publication.add_argument("--compiled", help="optional compiled.ai.md path")
    compiled_publication.add_argument("--output", help="optional publication output path; default: stdout")

    return p


def run(args: argparse.Namespace) -> int:
    if args.area == "capabilities":
        return emit_capabilities(args.json)

    root = repository_root(args.root)
    spec = root / "SEMANTIC_GIT.md"

    if args.area == "validate":
        validator = structure.Validator(root, spec)
        validator.run()
        validator.print_report(args.json)
        return 1 if validator.result() == "FAIL" else 0

    if args.area == "publication":
        target = namespace_dir(root, args.namespace)
        payload = publication_operation(root, target, spec, args)
        publication.emit(payload, args.json)
        return 0 if payload["status"] == "CURRENT" else 1

    if args.area == "index":
        namespace = namespace_value(args.namespace)
        if args.operation == "build":
            print(f"BUILT {index.rel(root, index.write_index(root, namespace))}")
            return 0
        if args.operation == "validate":
            path, errors = index.validate_index(root, namespace)
            if errors:
                print(f"FAIL {index.rel(root, path)}")
                for error in errors:
                    print(f"- {error}")
                return 1
            print(f"PASS {index.rel(root, path)}")
            return 0
        result = index.query_index(root, namespace, args.node_id, args.text, args.type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.area == "compiled":
        namespace = namespace_value(args.namespace)
        if args.operation == "build":
            path = compiled.build(root, namespace, user_path(root, args.output))
            print(f"BUILT {compiled.repo_relative(root, path)}")
            return 0
        if args.operation == "validate":
            path, errors = compiled.validate(root, namespace, user_path(root, args.compiled))
            if errors:
                print(f"FAIL {compiled.repo_relative(root, path)}")
                for error in errors:
                    print(f"- {error}")
                return 1
            print(f"PASS {compiled.repo_relative(root, path)}")
            return 0

        namespaces, _, _ = index.catalog(root)
        target = index.resolve_scope(root, namespace, namespaces)
        source = user_path(root, args.compiled) or target["path"] / "compiled.ai.md"
        projected = compiled.publication_projection(target["path"], compiled.read_text(source))
        output = user_path(root, args.output)
        if output:
            compiled.write_text(output, projected)
        else:
            sys.stdout.write(projected)
        return 0

    raise CliError("unknown capability")


def main() -> int:
    args = parser().parse_args()
    try:
        return run(args)
    except (CliError, publication.PublicationError, compiled.CompilationError, index.IndexErrorBase, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
