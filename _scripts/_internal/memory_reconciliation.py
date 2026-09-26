#!/usr/bin/env python3
"""Deterministically locate promoted findings impacted by a CHANGE Semantic Diff."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from . import semantic_index

AFFECTED_LOCAL_RE = re.compile(r"\b(?:MODIFY|REMOVE)\s+([RDO]-\d{3,})\b")
AFFECTED_CANONICAL_RE = re.compile(r"\b(?:MODIFY|REMOVE)\s+((?:root|[A-Za-z0-9][\w.-]*(?:/[A-Za-z0-9][\w.-]*)*):[RDO]-\d{3,})\b")


def affected_rdo_refs(change_text: str, controller_namespace: str) -> set[str]:
    refs = set(AFFECTED_CANONICAL_RE.findall(change_text))
    for local in AFFECTED_LOCAL_RE.findall(change_text):
        refs.add(f"{controller_namespace}:{local}")
    return refs


def controller_namespace(root: Path, change_path: Path) -> str:
    parent = change_path.resolve().parent
    if parent.name == "archived":
        parent = parent.parent
    if parent.name != "_changes":
        raise ValueError("CHANGE must live in a canonical _changes directory")
    return semantic_index.ns_id(root.resolve(), parent.parent.resolve())


def impacted_promoted_findings(root: Path, change_path: Path) -> dict[str, Any]:
    root = root.resolve()
    change_path = change_path.resolve()
    text = change_path.read_text(encoding="utf-8-sig")
    namespace = controller_namespace(root, change_path)
    affected = affected_rdo_refs(text, namespace)
    _nss, nodes, edges = semantic_index.catalog(root)
    impacted: list[dict[str, str]] = []
    for relation in edges:
        if relation.get("type") != "semantic_ref" or relation.get("to") not in affected:
            continue
        node = nodes.get(str(relation.get("from")))
        if not node or node.get("type") != "finding" or node.get("status") != "promoted":
            continue
        impacted.append({"finding": str(node["id"]), "semantic_ref": str(relation["to"]), "source": str(node.get("source", {}).get("path", ""))})
    impacted.sort(key=lambda item: (item["finding"], item["semantic_ref"]))
    return {"change": change_path.relative_to(root).as_posix(), "controller_namespace": namespace, "affected_rdo": sorted(affected), "impacted_promoted_findings": impacted}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--change", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    change = Path(args.change)
    if not change.is_absolute():
        change = root / change
    payload = impacted_promoted_findings(root, change)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"affected R/D/O: {len(payload['affected_rdo'])}")
        for item in payload["impacted_promoted_findings"]:
            print(f"{item['finding']} -> {item['semantic_ref']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
