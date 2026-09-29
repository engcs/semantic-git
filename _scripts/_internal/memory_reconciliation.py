#!/usr/bin/env python3
"""Deterministically locate and update FINDINGS relationships affected by semantic change."""
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
        if not node or node.get("type") != "finding" or node.get("status") not in {"promovido", "promoted"}:
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


def _rdo_refs(target: dict[str, Any]) -> list[str]:
    rdo = target.get("rdo")
    if isinstance(rdo, dict) and isinstance(rdo.get("referencias"), list):
        return [str(item) for item in rdo["referencias"]]
    legacy = target.get("semantic_refs")
    return [str(item) for item in legacy] if isinstance(legacy, list) else []


def upsert_human_clarification(
    findings: list[dict[str, Any]],
    finding_id: str,
    *,
    statement: str | None = None,
    summary: str | None = None,
    human_provenance: str,
    uncertain: bool = False,
    normative_intent: bool = False,
    potential_rdo_conflict: bool = False,
) -> dict[str, Any]:
    """Apply a human clarification after semantic equivalence resolved an existing F-*.

    Semantic equivalence is intentionally not decided here. The caller supplies
    the stable finding identity. Current PT-BR FINDINGS are updated in-place;
    the legacy English shape remains readable for historical test/recovery paths.
    """
    material = statement if statement is not None else summary
    if material is None:
        raise ValueError("statement must be provided")
    material = _compact_human_text(material, field="statement", limit=1200)
    provenance = _compact_human_text(human_provenance, field="human_provenance", limit=400)
    updated = deepcopy(findings)
    matches = [item for item in updated if str(item.get("id", "")) == finding_id]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one finding {finding_id}, found {len(matches)}")

    target = matches[0]
    current_shape = "afirmacao" in target or "evidencias" in target or "estado" in target
    previous_status = str(target.get("estado" if current_shape else "status", ""))
    refs = _rdo_refs(target)

    if current_shape:
        target["afirmacao"] = material
        evidence = target.setdefault("evidencias", {})
        if not isinstance(evidence, dict):
            raise ValueError("finding evidencias must be a mapping")
        samples = evidence.setdefault("amostras", [])
        if not isinstance(samples, list):
            raise ValueError("finding evidencias.amostras must be a list when present")
        sample = {
            "tipo": "clarificacao_humana",
            "fonte": "humano",
            "localizador": provenance,
            "amostra": material,
        }
        if sample not in samples:
            samples.append(sample)
    else:
        target["summary"] = material
        evidence = target.setdefault("evidence", {})
        if not isinstance(evidence, dict):
            raise ValueError("finding evidence must be a mapping")
        sources = evidence.setdefault("sources", [])
        if not isinstance(sources, list):
            raise ValueError("finding evidence.sources must be a list when present")
        source = {"type": "human_clarification", "locator": provenance}
        if source not in sources:
            sources.append(source)

    promoted = previous_status in {"promovido", "promoted"}
    reopened = promoted and bool(refs) and potential_rdo_conflict
    review_required = bool(uncertain or reopened)
    if review_required:
        if current_shape:
            target["estado"] = "ativo"
            semantics = target.setdefault("semantica", {})
            if not isinstance(semantics, dict):
                raise ValueError("finding semantica must be a mapping")
            semantics["estado"] = "nao_resolvido"
            semantics["motivo"] = "Clarificação humana preserva incerteza material ou reabre relação com R/D/O autoritativo."
            if reopened:
                rdo = target.setdefault("rdo", {})
                if not isinstance(rdo, dict):
                    raise ValueError("finding rdo must be a mapping")
                rdo["disposicao"] = "revisao"
        else:
            target["status"] = "active"
            semantic_status = target.setdefault("semantic_status", {})
            if not isinstance(semantic_status, dict):
                raise ValueError("finding semantic_status must be a mapping")
            semantic_status["state"] = "unresolved"
            semantic_status["reason"] = "Human clarification leaves a material uncertainty or reopens the relationship with authoritative R/D/O."

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
