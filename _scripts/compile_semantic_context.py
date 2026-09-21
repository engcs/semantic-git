#!/usr/bin/env python3
"""Build and validate deterministic per-domain Compiled Semantic Context files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import semantic_index as si

FORMAT_VERSION = 1
GENERATOR_VERSION = 1
SOURCE_ORDER = ("README.md", "REQUIREMENTS.md", "DECISIONS.md", "OPERATIONS.md")
RDO_TYPES = {"requirement", "decision", "operation"}
RELATION_TYPES = {"satisfies", "depends_on", "references", "semantic_ref"}
SOURCE_BEGIN_RE = re.compile(r"<!-- CSC-SOURCE-BEGIN (\{.*\}) -->\n")
SOURCE_END = "\n<!-- CSC-SOURCE-END -->"
SCRIPT_PATH = Path(__file__).resolve()
INDEXER_PATH = SCRIPT_PATH.with_name("semantic_index.py")


class CompilationError(RuntimeError):
    pass


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def read_text(path: Path) -> str:
    try:
        return normalize_text(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError) as error:
        raise CompilationError(f"cannot read {path}: {error}") from error


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(normalize_text(text), encoding="utf-8", newline="\n")


def digest_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def digest_file(path: Path) -> str:
    return digest_text(read_text(path))


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode:
        raise CompilationError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result


def repo_relative(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def assert_committed(repo_root: Path, paths: list[Path]) -> None:
    for path in sorted({p.resolve() for p in paths}):
        relative = repo_relative(repo_root, path)
        head = git(repo_root, "rev-parse", f"HEAD:{relative}", check=False)
        if head.returncode:
            raise CompilationError(f"compiled source is not committed at HEAD: {relative}")
        current = git(repo_root, "hash-object", "--", str(path)).stdout.strip()
        if current != head.stdout.strip():
            raise CompilationError(f"compiled source differs from HEAD: {relative}")


def local_source_texts(namespace_dir: Path) -> dict[str, str]:
    texts: dict[str, str] = {}
    for filename in SOURCE_ORDER:
        path = namespace_dir / filename
        if path.is_file():
            texts[filename] = read_text(path)
    if not any(name in texts for name in ("REQUIREMENTS.md", "DECISIONS.md", "OPERATIONS.md")):
        raise CompilationError("namespace has no local R/D/O source to compile")
    return texts


def _semantic_closure(
    namespace: str,
    nodes: dict[str, dict[str, Any]],
    edges: list[dict[str, str]],
) -> tuple[list[str], list[str], list[dict[str, str]], list[dict[str, str]]]:
    local = sorted(
        node_id
        for node_id, node in nodes.items()
        if node.get("namespace") == namespace and node.get("type") in RDO_TYPES
    )
    if not local:
        raise CompilationError(f"namespace {namespace} has no indexed local R/D/O nodes")

    outgoing: dict[str, list[dict[str, str]]] = {}
    for relation in edges:
        if relation.get("type") in RELATION_TYPES:
            outgoing.setdefault(relation.get("from", ""), []).append(relation)
    for relations in outgoing.values():
        relations.sort(key=lambda item: (item["type"], item["to"]))

    selected = set(local)
    external: set[str] = set()
    unresolved: list[dict[str, str]] = []
    queue = list(local)
    cursor = 0
    while cursor < len(queue):
        source = queue[cursor]
        cursor += 1
        for relation in outgoing.get(source, []):
            target = relation["to"]
            target_node = nodes.get(target)
            if target_node is None:
                unresolved.append(dict(relation))
                continue
            if target_node.get("type") not in RDO_TYPES:
                continue
            if target not in selected:
                selected.add(target)
                queue.append(target)
                if target_node.get("namespace") != namespace:
                    external.add(target)

    selected_edges = sorted(
        (
            dict(relation)
            for relation in edges
            if relation.get("type") in RELATION_TYPES
            and relation.get("from") in selected
            and relation.get("to") in selected
        ),
        key=lambda item: (item["from"], item["type"], item["to"]),
    )
    unresolved = sorted(unresolved, key=lambda item: (item["from"], item["type"], item["to"]))
    return local, sorted(external), selected_edges, unresolved


def _relations_by_node(node_ids: set[str], edges: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {node_id: [] for node_id in node_ids}
    for relation in edges:
        source, target, relation_type = relation["from"], relation["to"], relation["type"]
        if source in result:
            result[source].append({"direction": "out", "type": relation_type, "node": target})
        if target in result:
            result[target].append({"direction": "in", "type": relation_type, "node": source})
    for relations in result.values():
        relations.sort(key=lambda item: (item["direction"], item["type"], item["node"]))
    return result


def _fingerprint(
    source_texts: dict[str, str],
    local_ids: list[str],
    external_ids: list[str],
    nodes: dict[str, dict[str, Any]],
    edges: list[dict[str, str]],
) -> str:
    payload = {
        "sources": [{"path": name, "sha256": digest_text(source_texts[name])} for name in SOURCE_ORDER if name in source_texts],
        "local": local_ids,
        "external": [
            {
                "id": node_id,
                "type": nodes[node_id].get("type"),
                "text": nodes[node_id].get("text", ""),
                "source": nodes[node_id].get("source", {}),
            }
            for node_id in external_ids
        ],
        "edges": edges,
    }
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return digest_text(serialized)


def _render_source_block(filename: str, text: str) -> str:
    metadata = {
        "path": filename,
        "chars": len(text),
        "sha256": digest_text(text),
    }
    encoded = json.dumps(metadata, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return f"### {filename}\n<!-- CSC-SOURCE-BEGIN {encoded} -->\n{text}\n<!-- CSC-SOURCE-END -->\n"


def render_compiled(
    namespace: str,
    source_commit: str,
    source_texts: dict[str, str],
    nodes: dict[str, dict[str, Any]],
    local_ids: list[str],
    external_ids: list[str],
    edges: list[dict[str, str]],
    unresolved: list[dict[str, str]],
) -> str:
    selected_ids = set(local_ids) | set(external_ids)
    relations = _relations_by_node(selected_ids, edges)
    fingerprint = _fingerprint(source_texts, local_ids, external_ids, nodes, edges)

    lines = [
        "# COMPILED SEMANTIC CONTEXT",
        "",
        f"format: csc-md/{FORMAT_VERSION}",
        f"namespace: {namespace}",
        f"source_commit: {source_commit}",
        f"source_fingerprint: {fingerprint}",
        f"generator_version: {GENERATOR_VERSION}",
        f"generator_sha256: {digest_file(SCRIPT_PATH)}",
        f"indexer_sha256: {digest_file(INDEXER_PATH)}",
        "authority: DERIVED",
        "",
        "## Source Blocks",
        "",
    ]

    for filename in SOURCE_ORDER:
        if filename in source_texts:
            lines.append(_render_source_block(filename, source_texts[filename]).rstrip("\n"))
            lines.append("")

    lines.extend(["## Semantic Index", "", "```jsonl"])
    for node_id in local_ids:
        node = nodes[node_id]
        entry = {
            "id": node_id,
            "type": node["type"],
            "source": node.get("source", {}),
            "relations": relations.get(node_id, []),
        }
        lines.append(json.dumps(entry, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    lines.append("```")

    if external_ids:
        lines.extend(["", "## External Semantic Units", ""])
        for node_id in external_ids:
            node = nodes[node_id]
            lines.extend(
                [
                    f"### {node_id}",
                    "",
                    "```json",
                    json.dumps(
                        {
                            "id": node_id,
                            "type": node.get("type"),
                            "source": node.get("source", {}),
                            "relations": relations.get(node_id, []),
                        },
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    ),
                    "```",
                    "",
                    node.get("text", ""),
                    "",
                ]
            )

    if unresolved:
        lines.extend(["## Unresolved References", "", "```jsonl"])
        for relation in unresolved:
            lines.append(json.dumps(relation, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        lines.append("```")

    return "\n".join(lines).rstrip() + "\n"


def extract_source_texts(compiled_text: str) -> dict[str, str]:
    texts: dict[str, str] = {}
    cursor = 0
    while True:
        match = SOURCE_BEGIN_RE.search(compiled_text, cursor)
        if match is None:
            break
        try:
            metadata = json.loads(match.group(1))
            path = str(metadata["path"])
            length = int(metadata["chars"])
            expected_hash = str(metadata["sha256"])
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            raise CompilationError(f"invalid source block metadata: {error}") from error
        start = match.end()
        content = compiled_text[start : start + length]
        end = start + length
        if compiled_text[end : end + len(SOURCE_END)] != SOURCE_END:
            raise CompilationError(f"source block terminator mismatch: {path}")
        if digest_text(content) != expected_hash:
            raise CompilationError(f"source block checksum mismatch: {path}")
        if path in texts:
            raise CompilationError(f"duplicate source block: {path}")
        texts[path] = content
        cursor = end + len(SOURCE_END)
    if not texts:
        raise CompilationError("compiled file has no source blocks")
    return texts


def build_text(repo_root: Path, scope_value: str) -> tuple[Path, str]:
    repo_root = repo_root.resolve()
    si.validate_structure(repo_root)
    namespaces, nodes, all_edges = si.catalog(repo_root)
    scope = si.resolve_scope(repo_root, scope_value, namespaces)
    namespace_dir = scope["path"]
    source_texts = local_source_texts(namespace_dir)
    local_ids, external_ids, edges, unresolved = _semantic_closure(scope["id"], nodes, all_edges)

    source_paths = [namespace_dir / filename for filename in source_texts]
    for node_id in external_ids:
        source = nodes[node_id].get("source", {}).get("path")
        if source:
            source_paths.append(repo_root / source)
    assert_committed(repo_root, source_paths)
    relatives = sorted({repo_relative(repo_root, path) for path in source_paths})
    source_commit = git(repo_root, "log", "-1", "--format=%H", "--", *relatives).stdout.strip()
    if not source_commit:
        raise CompilationError("cannot resolve committed source snapshot")
    return namespace_dir / "compiled.ai.md", render_compiled(
        scope["id"],
        source_commit,
        source_texts,
        nodes,
        local_ids,
        external_ids,
        edges,
        unresolved,
    )


def build(repo_root: Path, scope_value: str, output: Path | None = None) -> Path:
    default_path, text = build_text(repo_root, scope_value)
    path = output.resolve() if output else default_path
    write_text(path, text)
    return path


def validate(repo_root: Path, scope_value: str, compiled_path: Path | None = None) -> tuple[Path, list[str]]:
    default_path, expected = build_text(repo_root, scope_value)
    path = compiled_path.resolve() if compiled_path else default_path
    if not path.is_file():
        return path, ["MISSING: compiled.ai.md does not exist"]
    try:
        actual = read_text(path)
        extract_source_texts(actual)
    except CompilationError as error:
        return path, [f"INVALID: {error}"]
    if actual != expected:
        return path, ["DRIFT: compiled.ai.md differs from deterministic regeneration"]
    return path, []


def publication_projection(namespace_dir: Path, compiled_text: str) -> str:
    import build_publication as bp

    texts = extract_source_texts(compiled_text)
    return bp.render_publication(namespace_dir, texts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="path inside the Semantic Repository")
    commands = parser.add_subparsers(dest="command", required=True)

    build_parser = commands.add_parser("build", help="generate compiled.ai.md")
    build_parser.add_argument("--scope", required=True, help="Semantic Namespace directory")
    build_parser.add_argument("--output", help="optional output path; defaults to <scope>/compiled.ai.md")

    validate_parser = commands.add_parser("validate", help="validate compiled.ai.md against deterministic regeneration")
    validate_parser.add_argument("--scope", required=True, help="Semantic Namespace directory")
    validate_parser.add_argument("--compiled", help="optional compiled file path")

    publication_parser = commands.add_parser("publication", help="project the current Markdown publication from compiled.ai.md")
    publication_parser.add_argument("--scope", required=True, help="Semantic Namespace directory")
    publication_parser.add_argument("--compiled", help="optional compiled file path")
    publication_parser.add_argument("--output", help="write publication to this path instead of stdout")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo_root = si.git_root(Path(args.root).expanduser().resolve())
        if args.command == "build":
            path = build(repo_root, args.scope, Path(args.output) if args.output else None)
            print(f"BUILT {repo_relative(repo_root, path)}")
            return 0
        if args.command == "validate":
            path, errors = validate(repo_root, args.scope, Path(args.compiled) if args.compiled else None)
            if errors:
                print(f"FAIL {repo_relative(repo_root, path)}")
                for error in errors:
                    print(f"- {error}")
                return 1
            print(f"PASS {repo_relative(repo_root, path)}")
            return 0

        namespaces, _, _ = si.catalog(repo_root)
        scope = si.resolve_scope(repo_root, args.scope, namespaces)
        compiled_path = Path(args.compiled).expanduser().resolve() if args.compiled else scope["path"] / "compiled.ai.md"
        compiled_text = read_text(compiled_path)
        publication = publication_projection(scope["path"], compiled_text)
        if args.output:
            write_text(Path(args.output).expanduser().resolve(), publication)
        else:
            sys.stdout.write(publication)
        return 0
    except (CompilationError, si.IndexErrorBase, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
