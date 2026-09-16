#!/usr/bin/env python3
"""Build and check a deterministic namespace publication."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import unicodedata
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
    display_name = first_heading(texts.get("README.md", "")) or root.name
    lines = [
        f"# GIT SEMÂNTICO - {display_name.upper()}",
        "",
    ]

    if "README.md" in texts:
        lines.extend([demote_headings(texts["README.md"], remove_first_h1=True, extra_levels=0), ""])

    for filename, label in RDO_SOURCES:
        lines.extend(["---", "", demote_headings(texts[filename], extra_levels=0), ""])

    return "\n".join(lines).rstrip() + "\n"


def first_heading(text: str) -> str:
    for line in text.splitlines():
        match = re.fullmatch(r"#(?!#)\s+(.+?)\s*", line)
        if match:
            return match.group(1)
    return ""


def publication_slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").upper()


def pdf_inline(value: str, code_font: str = "PublicationCode") -> str:
    value = html.escape(value)
    value = re.sub(r"`([^`]+)`", rf'<font name="{code_font}" color="#9A6B00">\1</font>', value)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)


def pdf_font_setup() -> tuple[str, str, str, str]:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    font_directory = Path("C:/Windows/Fonts")
    definitions = {
        "PublicationSans": ("segoeui.ttf", "Segoe UI"),
        "PublicationSans-Bold": ("segoeuib.ttf", "Segoe UI Bold"),
        "PublicationCode": ("consola.ttf", "Consolas"),
        "PublicationHeader": ("arial.ttf", "Arial"),
    }
    loaded: dict[str, bool] = {}
    for alias, (filename, _) in definitions.items():
        path = font_directory / filename
        if path.is_file():
            if alias not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(alias, str(path)))
            loaded[alias] = True

    body = "PublicationSans" if loaded.get("PublicationSans") else "Helvetica"
    bold = "PublicationSans-Bold" if loaded.get("PublicationSans-Bold") else "Helvetica-Bold"
    code = "PublicationCode" if loaded.get("PublicationCode") else "Courier"
    header = "PublicationHeader" if loaded.get("PublicationHeader") else "Helvetica"
    if body == "PublicationSans" and bold == "PublicationSans-Bold":
        pdfmetrics.registerFontFamily(body, normal=body, bold=bold)
    return body, bold, code, header


def pdf_source_flowables(text: str, body_style: Any, heading_style: Any, subheading_style: Any, item_style: Any, code_font: str) -> list[Any]:
    from reportlab.platypus import HRFlowable, Paragraph, Spacer

    result: list[Any] = []
    heading_count = 0
    previous_rule: str | None = None
    for line in text.splitlines():
        if not line.strip():
            result.append(Spacer(1, 5.5 if previous_rule == "separator" else 8))
            previous_rule = None
            continue
        if line.strip() == "---":
            result.append(HRFlowable(width="100%", thickness=2, color="#808080", spaceBefore=7, spaceAfter=0))
            previous_rule = "separator"
            continue
        heading = re.fullmatch(r"#\s+(.+?)\s*", line)
        if heading:
            heading_count += 1
            underline_gap = 14.6 if heading_count == 1 else 9.4
            result.extend([Paragraph(pdf_inline(heading.group(1), code_font), heading_style), HRFlowable(width="100%", thickness=0.6, color="#000000", spaceBefore=3, spaceAfter=underline_gap)])
            previous_rule = "heading"
            continue
        subheading = re.fullmatch(r"##\s+(.+?)\s*", line)
        if subheading:
            result.append(Paragraph(pdf_inline(subheading.group(1), code_font), subheading_style))
            continue
        item = re.fullmatch(r"-\s+\*\*([^*]+)\*\*\s+-\s+(.+)", line)
        if item:
            result.append(Paragraph(f"<b>{pdf_inline(item.group(1), code_font)}</b> - {pdf_inline(item.group(2), code_font)}", item_style, bulletText="•"))
            continue
        result.append(Paragraph(pdf_inline(line, code_font), body_style))
    return result


def write_pdf_reportlab(root: Path, texts: dict[str, str], pdf_path: Path) -> str | None:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.pdfgen import canvas
        from reportlab.platypus import Paragraph, SimpleDocTemplate
    except ImportError:
        return None

    body_font, bold_font, code_font, header_font = pdf_font_setup()
    styles = getSampleStyleSheet()
    body = ParagraphStyle("PublicationBody", parent=styles["BodyText"], fontName=body_font, fontSize=10.5, leading=16.5, textColor=colors.black, alignment=TA_LEFT, spaceBefore=0, spaceAfter=0)
    heading = ParagraphStyle("PublicationHeading", parent=styles["Heading1"], fontName=body_font, fontSize=21, leading=25.2, textColor=colors.black, alignment=TA_LEFT, spaceBefore=0, spaceAfter=0)
    subheading = ParagraphStyle("PublicationSubheading", parent=styles["Heading2"], fontName=body_font, fontSize=15.75, leading=16.5, textColor=colors.black, alignment=TA_LEFT, spaceBefore=1.4, spaceAfter=8.84)
    item = ParagraphStyle("PublicationItem", parent=body, fontName=body_font, leftIndent=30, firstLineIndent=0, bulletIndent=18, spaceBefore=0, spaceAfter=0)

    display_name = first_heading(texts.get("README.md", "")) or root.name
    footer_name = f"GIT_SEMANTICO_{publication_slug(display_name)}.md"
    page_size = (595.92, 841.92)

    class NumberedCanvas(canvas.Canvas):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            self.saved_pages: list[dict[str, Any]] = []

        def showPage(self) -> None:
            self.saved_pages.append(dict(self.__dict__))
            self._startPage()

        def save(self) -> None:
            total = len(self.saved_pages)
            for state in self.saved_pages:
                self.__dict__.update(state)
                self.saveState()
                self.setFillColor(colors.black)
                self.setFont(header_font, 6.75)
                self.drawString(10 * mm, page_size[1] - 20, footer_name)
                self.drawRightString(page_size[0] - 10 * mm, page_size[1] - 20, datetime.date.today().isoformat())
                self.drawCentredString(page_size[0] / 2, 17, f"{self._pageNumber} / {total}")
                self.restoreState()
                super().showPage()
            super().save()

    publication = render_publication(root, texts)
    story = pdf_source_flowables(publication, body, heading, subheading, item, code_font)

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(pdf_path), pagesize=page_size, rightMargin=13 * mm, leftMargin=13 * mm, topMargin=15 * mm, bottomMargin=8 * mm)
    document.build(story, canvasmaker=NumberedCanvas)
    return "reportlab"


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

    texts, sources = source_texts(root)
    markdown = render_publication(root, texts)
    paths = publication_paths(root)
    paths["directory"].mkdir(parents=True, exist_ok=True)
    write_text(paths["markdown"], markdown)

    pdf_engine: str | None = None
    if create_pdf:
        pdf_engine = write_pdf_reportlab(root, texts, paths["pdf"])
        if pdf_engine is None:
            pandoc = shutil.which("pandoc")
            if pandoc is None:
                raise PublicationError("--pdf requested but reportlab and pandoc are unavailable")
            result = subprocess.run(
                [pandoc, str(paths["markdown"]), "-o", str(paths["pdf"])],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                detail = result.stderr.strip() or result.stdout.strip() or "pandoc failed"
                raise PublicationError(detail)
            pdf_engine = "pandoc"

    manifest = base_manifest(root, spec, sources, digest_text(markdown))
    if create_pdf and paths["pdf"].is_file():
        manifest["pdf"] = {
            "path": paths["pdf"].relative_to(root).as_posix(),
            "sha256": digest_file(paths["pdf"], normalize=False),
            "publication_sha256": digest_text(markdown),
            "engine": pdf_engine,
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
    build_parser.add_argument("--pdf", action="store_true", help="also generate the PDF")

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
