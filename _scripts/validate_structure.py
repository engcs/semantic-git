#!/usr/bin/env python3
"""Validate the deterministic filesystem contract of a Semantic Repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


CANONICAL_DOCUMENTS = {
    "REQUIREMENTS.md": ("Requirements", "R"),
    "DECISIONS.md": ("Decisions", "D"),
    "OPERATIONS.md": ("Operations", "O"),
}
CANONICAL_NAMES = {
    "README.md",
    "REQUIREMENTS.md",
    "DECISIONS.md",
    "OPERATIONS.md",
    "SEMANTIC_GIT.md",
    "AGENTS.md",
    ".semantic-repo.yaml",
}
DOCUMENT_STEMS = {"requirements", "requirement", "decisions", "decision", "operations", "operation"}
CHANGE_FILE_RE = re.compile(r"^CHANGE-(?:INIT|\d{3,})\.md$")
CHANGE_ID_RE = re.compile(r"^CHANGE-(?:INIT|\d{3,})$")
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{7,64}$")
STATUS_VALUES = {"DRAFT", "APPROVED", "IN_PROGRESS", "RECONCILED", "MERGED", "ABANDONED"}
APPROVAL_STATUSES = {"APPROVED", "IN_PROGRESS", "RECONCILED", "MERGED"}
H1_RE = re.compile(r"^#(?!#)\s+(.+?)\s*$")
H2_RE = re.compile(r"^##(?!#)\s+(.+?)\s*$")
ITEM_RE = re.compile(r"^- \*\*([RDO]-\d{3,})\*\* - (.+\S)\s*$")
FIELD_RE = re.compile(r"^([a-z][a-z0-9_]*)\s*:\s*(.*?)\s*$")
FINDING_ID_RE = re.compile(r"^F-\d{3,}$")
FINDING_STATUS_VALUES = {"active", "resolved", "superseded", "promoted"}
FINDING_REQUIRED_FIELDS = {"id", "status", "category", "summary", "evidence", "risk", "semantic_status"}
FINDING_START_RE = re.compile(r"^  - id:\s*(\S.*?)\s*$")
FINDING_FIELD_RE = re.compile(r"^    ([a-z][a-z0-9_]*)\s*:\s*(.*?)\s*$")
INDEX_FILENAME = "SEMANTIC_INDEX.json"
INDEX_NODE_TYPES = {"namespace", "requirement", "decision", "operation", "change", "finding"}
INDEX_EDGE_TYPES = {"contains", "parent_namespace", "references", "satisfies", "depends_on", "semantic_ref"}


class Validator:
    def __init__(self, root: Path, spec: Path) -> None:
        self.root = root
        self.spec = spec
        self.findings: list[dict[str, Any]] = []
        self.rdo_count = 0
        self.change_count = 0
        self.memory_count = 0
        self.index_count = 0
        self.rdo_ids: dict[tuple[Path, str], dict[str, Path]] = {}

    def relative_path(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return path.resolve().as_posix()

    def add(self, rule: str, path: Path, message: str, line: int | None = None) -> None:
        finding: dict[str, Any] = {
            "result": "FAIL",
            "rule": rule,
            "path": self.relative_path(path),
            "message": message,
        }
        if line is not None:
            finding["line"] = line
        self.findings.append(finding)

    def run(self) -> None:
        self.validate_root()
        files, directories = self.inventory()
        self.validate_names(files)

        for path in files:
            if path.name in CANONICAL_DOCUMENTS:
                self.validate_rdo(path)

        for path in directories:
            if path.name.casefold() in {"_changes", "changes"}:
                self.validate_changes_directory(path)
            if path.name.casefold() in {"_memory", "memory"}:
                self.validate_memory_directory(path)
            if path.name.casefold() in {"_index", "index"}:
                self.validate_index_directory(path)

        self.validate_local_configuration()

    def validate_root(self) -> None:
        if not self.root.is_dir():
            self.add("ROOT", self.root, "validation root does not exist or is not a directory")
            return

        if not self.spec.is_file():
            self.add("SPEC_MISSING", self.spec, "SEMANTIC_GIT.md or the supplied normative spec was not found")

        result = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            self.add("GIT_ROOT", self.root, "validation root is not inside a Git repository")

    def inventory(self) -> tuple[list[Path], list[Path]]:
        files: list[Path] = []
        directories: list[Path] = []

        for current, dirnames, filenames in os.walk(self.root, followlinks=False):
            dirnames[:] = [name for name in dirnames if name not in {".git", "__pycache__"}]
            current_path = Path(current)
            directories.extend(current_path / name for name in dirnames)
            files.extend(current_path / name for name in filenames)

        return sorted(files), sorted(directories)

    def validate_names(self, files: list[Path]) -> None:
        canonical_by_case = {name.casefold(): name for name in CANONICAL_NAMES}
        for path in files:
            expected = canonical_by_case.get(path.name.casefold())
            if expected is not None and path.name != expected:
                self.add("CANONICAL_NAME", path, f"use the exact canonical name {expected}")

            if path.suffix.casefold() in {".md", ".markdown"} and path.stem.casefold() in DOCUMENT_STEMS:
                if path.name not in CANONICAL_DOCUMENTS:
                    self.add("CANONICAL_NAME", path, "dimension documents must use REQUIREMENTS.md, DECISIONS.md or OPERATIONS.md")

            if path.name.casefold() == "findings.yaml":
                if path.name != "FINDINGS.yaml":
                    self.add("MEMORY_FILENAME", path, "analytical memory must use the exact name FINDINGS.yaml")
                if path.parent.name != "_memory":
                    self.add("MEMORY_PATH", path, "FINDINGS.yaml is valid only inside a namespace _memory directory")

            if path.name.casefold() == INDEX_FILENAME.casefold():
                if path.name != INDEX_FILENAME:
                    self.add("INDEX_FILENAME", path, f"semantic index must use the exact name {INDEX_FILENAME}")
                if path.parent.name != "_index":
                    self.add("INDEX_PATH", path, f"{INDEX_FILENAME} is valid only inside a namespace _index directory")

    def read_lines(self, path: Path, rule: str) -> list[str] | None:
        try:
            return path.read_text(encoding="utf-8-sig").splitlines()
        except UnicodeDecodeError:
            self.add(rule, path, "file is not valid UTF-8")
        except OSError as error:
            self.add(rule, path, f"file could not be read: {error}")
        return None

    def validate_rdo(self, path: Path) -> None:
        self.rdo_count += 1
        lines = self.read_lines(path, "RDO_ENCODING")
        if lines is None:
            return
        if not any(line.strip() for line in lines):
            self.add("RDO_EMPTY", path, "R/D/O documents must not be empty")
            return

        label, prefix = CANONICAL_DOCUMENTS[path.name]
        h1 = [(number, match.group(1)) for number, line in enumerate(lines, 1) if (match := H1_RE.fullmatch(line))]
        h2 = [(number, match.group(1)) for number, line in enumerate(lines, 1) if (match := H2_RE.fullmatch(line))]
        header = [(number, title) for number, title in h2 if title == "Cabeçalho"]
        body = [(number, title) for number, title in h2 if title == "Corpo"]

        if len(h1) != 1:
            self.add("RDO_HEADINGS", path, "document must contain exactly one level-one heading")
        if len(header) != 1:
            self.add("RDO_HEADINGS", path, "document must contain exactly one ## Cabeçalho section")
        if len(body) != 1:
            self.add("RDO_HEADINGS", path, "document must contain exactly one ## Corpo section")

        all_heading_lines = [number for number, line in enumerate(lines, 1) if re.match(r"^#{1,6}\s", line)]
        allowed_heading_lines = {number for number, _ in h1} | {number for number, _ in h2 if _ in {"Cabeçalho", "Corpo"}}
        for number in all_heading_lines:
            if number not in allowed_heading_lines:
                self.add("RDO_HEADINGS", path, "additional headings are not allowed", number)

        if h1:
            title = h1[0][1]
            expected_prefix = f"{label} - "
            if not title.startswith(expected_prefix) or not title[len(expected_prefix) :].strip():
                self.add("RDO_TITLE", path, f"level-one heading must be # {expected_prefix}<namespace>", h1[0][0])

        if len(h1) == 1 and len(header) == 1 and len(body) == 1:
            h1_line = h1[0][0]
            header_line = header[0][0]
            body_line = body[0][0]
            if not h1_line < header_line < body_line:
                self.add("RDO_ORDER", path, "heading, Cabeçalho and Corpo must appear in that order")
            else:
                if any(line.strip() for line in lines[h1_line:header_line - 1]):
                    self.add("RDO_STRUCTURE", path, "no content is allowed between the title and Cabeçalho", h1_line + 1)
                if not any(line.strip() for line in lines[header_line:body_line - 1]):
                    self.add("RDO_STRUCTURE", path, "Cabeçalho must contain a summary", header_line)

                items = 0
                for number, line in enumerate(lines[body_line:], body_line + 1):
                    if not line.strip():
                        continue
                    match = ITEM_RE.fullmatch(line)
                    if match is None:
                        self.add("RDO_ITEMS", path, "Corpo must contain only direct items in the form - **X-001** - text", number)
                        continue
                    item_id = match.group(1)
                    items += 1
                    item_prefix = item_id[0]
                    if item_prefix != prefix:
                        self.add("RDO_ID_PREFIX", path, f"{path.name} items must use the {prefix}- prefix", number)
                        continue
                    namespace_key = (path.parent.resolve(), prefix)
                    previous = self.rdo_ids.setdefault(namespace_key, {}).get(item_id)
                    if previous is not None:
                        self.add("RDO_ID_DUPLICATE", path, f"{item_id} is duplicated in the same namespace and type; first occurrence: {self.relative_path(previous)}", number)
                    else:
                        self.rdo_ids[namespace_key][item_id] = path

                if items == 0:
                    self.add("RDO_ITEMS", path, "Corpo must contain at least one entity item", body_line)

        first_content = next((line.strip() for line in lines if line.strip()), "")
        if first_content == "---":
            self.add("RDO_FRONTMATTER", path, "frontmatter is not allowed in R/D/O documents", 1)

    def validate_changes_directory(self, changes_dir: Path) -> None:
        if changes_dir.name != "_changes":
            self.add("CHANGE_DIRECTORY", changes_dir, "the directory must be named exactly _changes")

        archived_dirs = [entry for entry in changes_dir.iterdir() if entry.is_dir() and entry.name.casefold() == "archived"]
        for archived_dir in archived_dirs:
            if archived_dir.name != "archived":
                self.add("CHANGE_DIRECTORY", archived_dir, "the archive directory must be named exactly archived")

        for entry in changes_dir.iterdir():
            if entry.is_dir():
                if entry.name.casefold() != "archived":
                    self.add("CHANGE_PATH", entry, "_changes may contain only files or the archived directory")
                continue
            self.validate_change_file(entry, archived=False)

        for archived_dir in archived_dirs:
            for entry in archived_dir.iterdir():
                if entry.is_dir():
                    self.add("CHANGE_PATH", entry, "archived changes may not contain nested directories")
                else:
                    self.validate_change_file(entry, archived=True)

        seen: dict[str, Path] = {}
        for entry in changes_dir.iterdir():
            if entry.is_file() and CHANGE_FILE_RE.fullmatch(entry.name):
                seen[entry.stem] = entry
        for archived_dir in archived_dirs:
            for entry in archived_dir.iterdir():
                if entry.is_file() and CHANGE_FILE_RE.fullmatch(entry.name):
                    previous = seen.get(entry.stem)
                    if previous is not None:
                        self.add("CHANGE_DUPLICATE_PATH", entry, f"the same CHANGE exists in active and archived paths: {self.relative_path(previous)}")
                    else:
                        seen[entry.stem] = entry

    def validate_change_file(self, path: Path, archived: bool) -> None:
        self.change_count += 1
        if not CHANGE_FILE_RE.fullmatch(path.name):
            self.add("CHANGE_FILENAME", path, "CHANGE files must be named CHANGE-INIT.md or CHANGE-NNN.md")
            return

        lines = self.read_lines(path, "CHANGE_ENCODING")
        if lines is None:
            return
        metadata, lists = self.parse_change_metadata(path, lines)

        change_id = metadata.get("change", "")
        status = metadata.get("status", "")
        base_commit = metadata.get("base_commit", "")

        if not CHANGE_ID_RE.fullmatch(change_id):
            self.add("CHANGE_CONTRACT", path, "change must be CHANGE-INIT or CHANGE-NNN")
        elif change_id != path.stem:
            self.add("CHANGE_CONTRACT", path, "change must match the filename", self.metadata_line(lines, "change"))

        if status not in STATUS_VALUES:
            self.add("CHANGE_STATUS", path, "status is not a canonical Semantic Git status", self.metadata_line(lines, "status"))
        if not COMMIT_RE.fullmatch(base_commit):
            self.add("CHANGE_CONTRACT", path, "base_commit must contain a hexadecimal Git commit identifier", self.metadata_line(lines, "base_commit"))

        if archived is False and status == "MERGED":
            self.add("CHANGE_ARCHIVE", path, "a MERGED CHANGE cannot remain in the active _changes directory", self.metadata_line(lines, "status"))

        if status in APPROVAL_STATUSES:
            approved_commit = metadata.get("approved_semantic_commit", "")
            if not COMMIT_RE.fullmatch(approved_commit):
                self.add("CHANGE_APPROVAL", path, "approved_semantic_commit is required after approval", self.metadata_line(lines, "approved_semantic_commit"))
            if not lists.get("approval_scope"):
                self.add("CHANGE_APPROVAL", path, "approval_scope must contain at least one path after approval", self.metadata_line(lines, "approval_scope"))

    def parse_change_metadata(self, path: Path, lines: list[str]) -> tuple[dict[str, str], dict[str, list[str]]]:
        metadata: dict[str, str] = {}
        lists: dict[str, list[str]] = {}
        current_list: str | None = None
        for number, line in enumerate(lines, 1):
            if re.match(r"^#{1,6}\s", line):
                break
            if not line.strip():
                continue
            if line.startswith("  - "):
                if current_list is None:
                    self.add("CHANGE_CONTRACT", path, "list item has no preceding metadata field", number)
                else:
                    lists.setdefault(current_list, []).append(line[4:].strip())
                continue

            match = FIELD_RE.fullmatch(line)
            if match is None:
                self.add("CHANGE_CONTRACT", path, "metadata before the first heading must use key: value lines", number)
                current_list = None
                continue

            key, value = match.groups()
            if key in metadata or key in lists:
                self.add("CHANGE_CONTRACT", path, f"metadata field {key} is duplicated", number)
            current_list = key if key in {"approval_scope", "depends_on"} and not value else None
            if key in {"approval_scope", "depends_on"} and not value:
                lists.setdefault(key, [])
            else:
                metadata[key] = value

        return metadata, lists

    @staticmethod
    def metadata_line(lines: list[str], key: str) -> int | None:
        prefix = f"{key}:"
        for number, line in enumerate(lines, 1):
            if line.startswith(prefix):
                return number
        return None

    def validate_memory_directory(self, memory_dir: Path) -> None:
        if memory_dir.name != "_memory":
            self.add("MEMORY_DIRECTORY", memory_dir, "the analytical memory directory must be named exactly _memory")

        entries = list(memory_dir.iterdir())
        if not entries:
            self.add("MEMORY_EMPTY", memory_dir, "_memory must not exist without at least one material finding")
            return

        for entry in entries:
            if entry.is_dir():
                self.add("MEMORY_PATH", entry, "_memory may contain only FINDINGS.yaml")
            elif entry.name != "FINDINGS.yaml":
                self.add("MEMORY_PATH", entry, "_memory may contain only the canonical FINDINGS.yaml file")

        findings_file = memory_dir / "FINDINGS.yaml"
        if not findings_file.is_file():
            self.add("MEMORY_FILE", memory_dir, "_memory must contain FINDINGS.yaml")
            return

        self.validate_memory_file(findings_file)

    def validate_memory_file(self, path: Path) -> None:
        self.memory_count += 1
        lines = self.read_lines(path, "MEMORY_ENCODING")
        if lines is None:
            return
        if not any(line.strip() for line in lines):
            self.add("MEMORY_EMPTY", path, "FINDINGS.yaml must contain at least one material finding")
            return

        namespace_lines = [(number, line.split(":", 1)[1].strip()) for number, line in enumerate(lines, 1) if line.startswith("namespace:")]
        if len(namespace_lines) != 1 or not namespace_lines[0][1]:
            self.add("MEMORY_CONTRACT", path, "FINDINGS.yaml must contain exactly one non-empty top-level namespace field")

        findings_lines = [number for number, line in enumerate(lines, 1) if line.strip() == "findings:"]
        if len(findings_lines) != 1:
            self.add("MEMORY_CONTRACT", path, "FINDINGS.yaml must contain exactly one top-level findings sequence")
            return

        findings_start = findings_lines[0]
        starts: list[tuple[int, str]] = []
        for number, line in enumerate(lines[findings_start:], findings_start + 1):
            match = FINDING_START_RE.fullmatch(line)
            if match:
                starts.append((number, match.group(1)))

        if not starts:
            self.add("MEMORY_EMPTY", path, "FINDINGS.yaml must contain at least one finding in the form '  - id: F-001'", findings_start)
            return

        seen_ids: dict[str, int] = {}
        for index, (start_line, finding_id) in enumerate(starts):
            end_line = starts[index + 1][0] - 1 if index + 1 < len(starts) else len(lines)
            if not FINDING_ID_RE.fullmatch(finding_id):
                self.add("MEMORY_ID", path, "finding id must use F-NNN with at least three decimal digits", start_line)
            elif finding_id in seen_ids:
                self.add("MEMORY_ID_DUPLICATE", path, f"{finding_id} is duplicated; first occurrence is line {seen_ids[finding_id]}", start_line)
            else:
                seen_ids[finding_id] = start_line

            fields: dict[str, tuple[int, str]] = {"id": (start_line, finding_id)}
            for number in range(start_line + 1, end_line + 1):
                match = FINDING_FIELD_RE.fullmatch(lines[number - 1])
                if not match:
                    continue
                key, value = match.groups()
                if key in fields:
                    self.add("MEMORY_CONTRACT", path, f"finding {finding_id} duplicates field {key}", number)
                else:
                    fields[key] = (number, value)

            missing = sorted(FINDING_REQUIRED_FIELDS - set(fields))
            for field in missing:
                self.add("MEMORY_CONTRACT", path, f"finding {finding_id} is missing required field {field}", start_line)

            status = fields.get("status")
            if status is not None and status[1] not in FINDING_STATUS_VALUES:
                self.add("MEMORY_STATUS", path, f"finding {finding_id} status must be one of {sorted(FINDING_STATUS_VALUES)}", status[0])

            for required_scalar in ("category", "summary"):
                field = fields.get(required_scalar)
                if field is not None and not field[1]:
                    self.add("MEMORY_CONTRACT", path, f"finding {finding_id} field {required_scalar} must not be empty", field[0])

    def validate_index_directory(self, index_dir: Path) -> None:
        if index_dir.name != "_index":
            self.add("INDEX_DIRECTORY", index_dir, "the semantic index directory must be named exactly _index")

        entries = list(index_dir.iterdir())
        if not entries:
            self.add("INDEX_EMPTY", index_dir, "_index must not exist without SEMANTIC_INDEX.json")
            return
        for entry in entries:
            if entry.is_dir():
                self.add("INDEX_PATH", entry, "_index may contain only SEMANTIC_INDEX.json")
            elif entry.name != INDEX_FILENAME:
                self.add("INDEX_PATH", entry, "_index may contain only the canonical SEMANTIC_INDEX.json file")

        index_file = index_dir / INDEX_FILENAME
        if not index_file.is_file():
            self.add("INDEX_FILE", index_dir, "_index must contain SEMANTIC_INDEX.json")
            return

        self.index_count += 1
        try:
            payload = json.loads(index_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            self.add("INDEX_JSON", index_file, f"semantic index is not valid UTF-8 JSON: {error}")
            return

        if payload.get("schema_version") != 1:
            self.add("INDEX_SCHEMA", index_file, "semantic index schema_version must be 1")
        scope = payload.get("scope")
        if not isinstance(scope, dict) or not scope.get("identity") or not scope.get("path"):
            self.add("INDEX_SCOPE", index_file, "semantic index scope must contain identity and path")
        source_commit = payload.get("source_commit")
        if not isinstance(source_commit, str) or not COMMIT_RE.fullmatch(source_commit):
            self.add("INDEX_SOURCE", index_file, "semantic index source_commit must be a Git commit identifier")
        fingerprint = payload.get("source_fingerprint")
        if not isinstance(fingerprint, str) or re.fullmatch(r"[0-9a-f]{64}", fingerprint) is None:
            self.add("INDEX_SOURCE", index_file, "semantic index source_fingerprint must be a SHA-256 hex string")

        nodes = payload.get("nodes")
        edges = payload.get("edges")
        if not isinstance(nodes, list):
            self.add("INDEX_NODES", index_file, "semantic index nodes must be an array")
            nodes = []
        if not isinstance(edges, list):
            self.add("INDEX_EDGES", index_file, "semantic index edges must be an array")
            edges = []

        ids: set[str] = set()
        node_map: dict[str, dict[str, Any]] = {}
        for node in nodes:
            if not isinstance(node, dict):
                self.add("INDEX_NODES", index_file, "every semantic index node must be an object")
                continue
            node_id = node.get("id")
            if not isinstance(node_id, str) or not node_id:
                self.add("INDEX_NODES", index_file, "every semantic index node must have a non-empty id")
                continue
            if node_id in ids:
                self.add("INDEX_NODE_DUPLICATE", index_file, f"semantic index node id is duplicated: {node_id}")
            ids.add(node_id)
            node_map[node_id] = node
            if node.get("type") not in INDEX_NODE_TYPES:
                self.add("INDEX_NODE_TYPE", index_file, f"semantic index node has unknown type: {node_id}")
            source = node.get("source")
            if not isinstance(source, dict) or not source.get("path") or not source.get("locator"):
                self.add("INDEX_SOURCE", index_file, f"semantic index node lacks source.path/source.locator: {node_id}")
            else:
                source_path = self.root if source["path"] == "." else self.root / str(source["path"])
                if not source_path.exists():
                    self.add("INDEX_SOURCE", index_file, f"semantic index node source does not exist: {source['path']}")
            if node.get("external") not in {None, True}:
                self.add("INDEX_EXTERNAL", index_file, f"external marker must be true when present: {node_id}")

        seen_edges: set[tuple[Any, Any, Any]] = set()
        for relation in edges:
            if not isinstance(relation, dict):
                self.add("INDEX_EDGES", index_file, "every semantic index edge must be an object")
                continue
            key = (relation.get("from"), relation.get("type"), relation.get("to"))
            if key in seen_edges:
                self.add("INDEX_EDGE_DUPLICATE", index_file, f"semantic index edge is duplicated: {key}")
            seen_edges.add(key)
            if relation.get("type") not in INDEX_EDGE_TYPES:
                self.add("INDEX_EDGE_TYPE", index_file, f"semantic index edge has unknown type: {relation.get('type')}")
            if relation.get("from") not in ids:
                self.add("INDEX_ENDPOINT", index_file, f"semantic index edge source does not exist: {relation.get('from')}")
            if relation.get("to") not in ids:
                self.add("INDEX_ENDPOINT", index_file, f"semantic index edge target does not exist: {relation.get('to')}")
            origin = node_map.get(str(relation.get("from")))
            if origin is not None and origin.get("external") is True:
                self.add("INDEX_EXTERNAL", index_file, f"external stub must not originate edges: {relation.get('from')}")

    def validate_local_configuration(self) -> None:
        result = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return
        git_root = Path(result.stdout.strip()).resolve()
        local_config = git_root / ".semantic-repo.local.yaml"
        if not local_config.is_file():
            return

        tracked = subprocess.run(
            ["git", "-C", str(git_root), "ls-files", "--error-unmatch", "--", ".semantic-repo.local.yaml"],
            capture_output=True,
            text=True,
            check=False,
        )
        if tracked.returncode == 0:
            self.add("LOCAL_CONFIG", local_config, ".semantic-repo.local.yaml must not be versioned")

        ignored = subprocess.run(
            ["git", "-C", str(git_root), "check-ignore", "--quiet", "--", ".semantic-repo.local.yaml"],
            capture_output=True,
            text=True,
            check=False,
        )
        if ignored.returncode != 0:
            self.add("LOCAL_CONFIG", local_config, ".semantic-repo.local.yaml must be ignored")

    def result(self) -> str:
        return "FAIL" if self.findings else "PASS"

    def payload(self) -> dict[str, Any]:
        return {
            "result": self.result(),
            "root": str(self.root),
            "spec": str(self.spec),
            "rdo_documents": self.rdo_count,
            "change_files": self.change_count,
            "memory_files": self.memory_count,
            "index_files": self.index_count,
            "findings": self.findings,
        }

    def print_report(self, as_json: bool) -> None:
        payload = self.payload()
        if as_json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return

        print(
            f"{payload['result']}: checked {self.rdo_count} R/D/O documents, "
            f"{self.change_count} CHANGE files, {self.memory_count} memory files and "
            f"{self.index_count} semantic index files"
        )
        for finding in self.findings:
            location = finding["path"]
            if "line" in finding:
                location = f"{location}:{finding['line']}"
            print(f"FAIL [{finding['rule']}] {location}: {finding['message']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="directory to validate")
    parser.add_argument("--spec", help="path to SEMANTIC_GIT.md when it is outside --root")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    spec = Path(args.spec).expanduser().resolve() if args.spec else root / "SEMANTIC_GIT.md"
    validator = Validator(root, spec)
    validator.run()
    validator.print_report(args.json)
    return 1 if validator.result() == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
