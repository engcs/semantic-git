#!/usr/bin/env python3
"""Build and check a deterministic namespace publication."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


RDO_SOURCES = (
    ("REQUIREMENTS.md", "REQUIREMENTS"),
    ("DECISIONS.md", "DECISIONS"),
    ("OPERATIONS.md", "OPERATIONS"),
)
FORMAT_VERSION = 1
SCRIPT_PATH = Path(__file__).resolve()
HEADING_RE = re.compile(r"^(#{1,6})(\s+.*)$")
H1_RE = re.compile(r"^#(?!#)\s+")


class PublicationError(Exception):
    pass


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def read_text(path: Path) -> str:
    try:
        return normalize_text(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError) as error:
        raise PublicationError(f"cannot read {path}: {error}") from error


def digest_text(text: str) -> str:
    value = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"sha256:{value}"


def digest_file(path: Path, normalize: bool = True) -> str:
    if normalize:
        return digest_text(read_text(path))
    try:
        value = hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise PublicationError(f"cannot read {path}: {error}") from error
    return f"sha256:{value}"


def write_text(path: Path, text: str) -> None:
    try:
        with path.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(normalize_text(text))
    except OSError as error:
        raise PublicationError(f"cannot write {path}: {error}") from error


def relative_label(path: Path, root: Path, fallback_prefix: str) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return f"{fallback_prefix}:{path.name}"


def publication_paths(root: Path) -> dict[str, Path]:
    directory = root / "_publications"
    return {
        "directory": directory,
        "markdown": directory / "PUBLICATION.md",
        "manifest": directory / "PUBLICATION.manifest.json",
        "pdf": directory / "PUBLICATION.pdf",
    }


def source_texts(root: Path) -> tuple[dict[str, str], list[dict[str, str]]]:
    texts: dict[str, str] = {}
    sources: list[dict[str, str]] = []

    readme = root / "README.md"
    if readme.is_file():
        texts["README.md"] = read_text(readme)
        sources.append({"path": "README.md", "sha256": digest_text(texts["README.md"])})

    for filename, _ in RDO_SOURCES:
        path = root / filename
        if not path.is_file():
            raise PublicationError(f"required source is missing: {filename}")
        texts[filename] = read_text(path)
        sources.append({"path": filename, "sha256": digest_text(texts[filename])})

    return texts, sources


def demote_headings(text: str, remove_first_h1: bool = False, extra_levels: int = 1) -> str:
    lines = text.splitlines()
    if remove_first_h1:
        for index, line in enumerate(lines):
            if H1_RE.match(line):
                lines = lines[index + 1 :]
                break

    result: list[str] = []
    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            level = min(6, len(match.group(1)) + extra_levels)
            result.append(f"{'#' * level}{match.group(2)}")
        else:
            result.append(line)
    return "\n".join(result).strip()


def render_publication(root: Path, texts: dict[str, str]) -> str:
    lines = [
        f"# {root.name}",
        "",
        "<!-- Generated publication. Do not edit manually. -->",
        "",
    ]

    if "README.md" in texts:
        lines.extend(["## README", "", demote_headings(texts["README.md"], extra_levels=2), ""])

    for filename, label in RDO_SOURCES:
        lines.extend([f"## {label}", "", demote_headings(texts[filename], remove_first_h1=True), ""])

    return "\n".join(lines).rstrip() + "\n"


def run_validator(root: Path, spec: Path) -> dict[str, Any]:
    validator = SCRIPT_PATH.with_name("validate_structure.py")
    if not validator.is_file():
        raise PublicationError(f"structure validator is missing: {validator}")

    result = subprocess.run(
        [sys.executable, str(validator), "--root", str(root), "--spec", str(spec), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        detail = result.stderr.strip() or result.stdout.strip() or "no validator output"
        raise PublicationError(f"structure validator failed: {detail}") from error

    if result.returncode != 0 or payload.get("result") == "FAIL":
        raise PublicationError("structure validation returned FAIL")
    return payload


def base_manifest(root: Path, spec: Path, sources: list[dict[str, str]], markdown_hash: str) -> dict[str, Any]:
    paths = publication_paths(root)
    return {
        "format": FORMAT_VERSION,
        "namespace": root.name,
        "sources": sources,
        "spec": {
            "path": relative_label(spec, root, "external"),
            "sha256": digest_file(spec),
        },
        "generator": {
            "path": "_scripts/build_publication.py",
            "sha256": digest_file(SCRIPT_PATH),
        },
        "publication": {
            "path": paths["markdown"].relative_to(root).as_posix(),
            "sha256": markdown_hash,
        },
    }


def manifest_matches_current(manifest: dict[str, Any], expected: dict[str, Any]) -> bool:
    for key in ("format", "namespace", "sources", "spec", "generator", "publication"):
        if manifest.get(key) != expected.get(key):
            return False
    return True


def build(root: Path, spec: Path, create_pdf: bool) -> dict[str, Any]:
    run_validator(root, spec)
    if not spec.is_file():
        raise PublicationError(f"normative spec is missing: {spec}")
    if create_pdf and shutil.which("pandoc") is None:
        raise PublicationError("--pdf requested but pandoc is not available")

    texts, sources = source_texts(root)
    markdown = render_publication(root, texts)
    paths = publication_paths(root)
    paths["directory"].mkdir(parents=True, exist_ok=True)
    write_text(paths["markdown"], markdown)

    if create_pdf:
        result = subprocess.run(
            [shutil.which("pandoc") or "pandoc", str(paths["markdown"]), "-o", str(paths["pdf"])],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip() or "pandoc failed"
            raise PublicationError(detail)

    manifest = base_manifest(root, spec, sources, digest_text(markdown))
    if create_pdf and paths["pdf"].is_file():
        manifest["pdf"] = {
            "path": paths["pdf"].relative_to(root).as_posix(),
            "sha256": digest_file(paths["pdf"], normalize=False),
            "publication_sha256": digest_text(markdown),
        }
    write_text(paths["manifest"], json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    status = "STALE" if paths["pdf"].is_file() and not create_pdf else "CURRENT"
    payload: dict[str, Any] = {"status": status, "root": str(root), "manifest": str(paths["manifest"]), "publication": str(paths["markdown"])}
    if status == "STALE":
        payload["reason"] = "PUBLICATION.pdf was not regenerated; run build with --pdf"
    return payload


def check_status(root: Path, spec: Path) -> dict[str, Any]:
    validation_error: str | None = None
    try:
        run_validator(root, spec)
    except PublicationError as error:
        validation_error = str(error)

    paths = publication_paths(root)
    if validation_error:
        return {"status": "INVALID", "root": str(root), "reason": validation_error}
    if not paths["markdown"].is_file() or not paths["manifest"].is_file():
        return {"status": "MISSING", "root": str(root), "publication": str(paths["markdown"]), "manifest": str(paths["manifest"])}

    try:
        manifest = json.loads(read_text(paths["manifest"]))
        texts, sources = source_texts(root)
        expected_markdown = render_publication(root, texts)
        expected = base_manifest(root, spec, sources, digest_text(expected_markdown))
    except (OSError, json.JSONDecodeError, PublicationError) as error:
        return {"status": "DRIFT", "root": str(root), "reason": str(error)}

    if not manifest_matches_current(manifest, expected):
        return {"status": "STALE", "root": str(root), "reason": "sources, spec or generator changed"}
    if digest_text(read_text(paths["markdown"])) != manifest["publication"].get("sha256"):
        return {"status": "DRIFT", "root": str(root), "reason": "PUBLICATION.md differs from its manifest"}
    if expected_markdown != read_text(paths["markdown"]):
        return {"status": "DRIFT", "root": str(root), "reason": "PUBLICATION.md differs from deterministic output"}

    pdf_entry = manifest.get("pdf")
    if pdf_entry:
        if pdf_entry.get("publication_sha256") != manifest["publication"].get("sha256"):
            return {"status": "STALE", "root": str(root), "reason": "PUBLICATION.pdf was generated from an older Markdown publication"}
        if not paths["pdf"].is_file() or digest_file(paths["pdf"], normalize=False) != pdf_entry.get("sha256"):
            return {"status": "DRIFT", "root": str(root), "reason": "PUBLICATION.pdf differs from its manifest"}
    elif paths["pdf"].is_file():
        return {"status": "STALE", "root": str(root), "reason": "PUBLICATION.pdf is not represented by the manifest"}

    return {"status": "CURRENT", "root": str(root), "publication": str(paths["markdown"]), "manifest": str(paths["manifest"])}


def add_root_and_spec(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", required=True, help="namespace directory to compile")
    parser.add_argument("--spec", help="path to SEMANTIC_GIT.md")
    parser.add_argument("--json", action="store_true", help="emit JSON")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    build_parser = commands.add_parser("build", help="generate the publication")
    add_root_and_spec(build_parser)
    build_parser.add_argument("--pdf", action="store_true", help="also convert with pandoc")

    status_parser = commands.add_parser("status", help="check publication freshness")
    add_root_and_spec(status_parser)
    return parser.parse_args()


def emit(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"{payload['status']}: {payload.get('root', '')}")
        if payload.get("reason"):
            print(f"  {payload['reason']}")
        if payload.get("publication"):
            print(f"  publication: {payload['publication']}")
        if payload.get("manifest"):
            print(f"  manifest: {payload['manifest']}")


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    spec = Path(args.spec).expanduser().resolve() if args.spec else root / "SEMANTIC_GIT.md"

    try:
        payload = build(root, spec, args.pdf) if args.command == "build" else check_status(root, spec)
    except (OSError, PublicationError) as error:
        payload = {"status": "INVALID", "root": str(root), "reason": str(error)}

    emit(payload, args.json)
    return 0 if payload["status"] == "CURRENT" else 1


if __name__ == "__main__":
    sys.exit(main())
