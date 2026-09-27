#!/usr/bin/env python3
"""Deterministically locate promoted findings impacted by a CHANGE Semantic Diff."""
from __future__ import annotations

import argparse
from copy import deepcopy
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



def _compact_human_text(value: str, *, field: str, limit: int) -> str:
    compact = " ".join(str(value).split())
    if not compact:
        raise ValueError(f"{field} must not be empty")
    if len(compact) > limit:
        raise ValueError(f"{field} is too long for analytical memory; store a material synthesis, not a transcript")
    return compact


def upsert_human_clarification(
    findings: list[dict[str, Any]],
    finding_id: str,
    *,
    summary: str,
    human_provenance: str,
    uncertain: bool = False,
    normative_intent: bool = False,
    potential_rdo_conflict: bool = False,
) -> dict[str, Any]:
    """Apply a human clarification after semantic equivalence resolved an existing F-*.

    This helper is deliberately deterministic: it does not decide whether two
    findings are semantically equivalent. The caller supplies the already-resolved
    finding identity; the function preserves that identity and unrelated findings.
    """
    summary = _compact_human_text(summary, field="summary", limit=1200)
    provenance = _compact_human_text(human_provenance, field="human_provenance", limit=400)
    updated = deepcopy(findings)
    matches = [item for item in updated if str(item.get("id", "")) == finding_id]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one finding {finding_id}, found {len(matches)}")

    target = matches[0]
    previous_status = str(target.get("status", ""))
    semantic_refs = target.get("semantic_refs")
    has_semantic_refs = isinstance(semantic_refs, list) and bool(semantic_refs)

    target["summary"] = summary
    evidence = target.setdefault("evidence", {})
    if not isinstance(evidence, dict):
        raise ValueError("finding evidence must be a mapping")
    sources = evidence.setdefault("sources", [])
    if not isinstance(sources, list):
        raise ValueError("finding evidence.sources must be a list when present")
    source = {"type": "human_clarification", "locator": provenance}
    if source not in sources:
        sources.append(source)

    reopened = previous_status == "promoted" and has_semantic_refs and potential_rdo_conflict
    review_required = bool(uncertain or reopened)
    if review_required:
        target["status"] = "active"
        semantic_status = target.setdefault("semantic_status", {})
        if not isinstance(semantic_status, dict):
            raise ValueError("finding semantic_status must be a mapping")
        semantic_status["state"] = "unresolved"
        semantic_status["reason"] = (
            "Human clarification leaves a material uncertainty or reopens the relationship with authoritative R/D/O."
        )

    return {
        "findings": updated,
        "finding_id": finding_id,
        "review_required": review_required,
        "rdo_reconciliation_required": reopened,
        "promotion_requires_change": bool(normative_intent),
    }


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
