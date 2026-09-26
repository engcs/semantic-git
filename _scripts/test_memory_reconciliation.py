#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _scripts._internal import memory_reconciliation as mod
from _scripts._internal.validate_structure import CANONICAL_RDO_REF_RE

ROOT = Path(__file__).resolve().parents[1]


def write_fixture(root: Path, *, status: str, semantic_ref: str, change_body: str, include_unrelated: bool = True) -> Path:
    (root / "_changes").mkdir(parents=True)
    (root / "DECISIONS.md").write_text(
        "# Decisions - Root\n\n## Cabeçalho\n\nTeste.\n\n## Corpo\n\n"
        "- **D-001** - Regra original.\n"
        "- **D-002** - Regra substituta.\n",
        encoding="utf-8",
    )
    memory = root / "_memory"
    memory.mkdir()
    findings = [
        "namespace: root",
        "findings:",
        "  - id: F-001",
        f"    status: {status}",
        "    category: physical_exception",
        "    summary: descoberta ligada à decisão",
        "    evidence:",
        "      certainty: proven",
        "    risk:",
        "      level: high",
        "    semantic_status:",
        f"      state: {'promoted' if status == 'promoted' else 'unresolved'}",
        "    semantic_refs:",
        f"      - {semantic_ref}",
    ]
    if include_unrelated:
        findings += [
            "  - id: F-002",
            "    status: promoted",
            "    category: historical_context",
            "    summary: descoberta não relacionada",
            "    evidence:",
            "      certainty: proven",
            "    risk:",
            "      level: low",
            "    semantic_status:",
            "      state: promoted",
            "    semantic_refs:",
            "      - root:D-002",
        ]
    (memory / "FINDINGS.yaml").write_text("\n".join(findings) + "\n", encoding="utf-8")
    change = root / "_changes/CHANGE-001.md"
    change.write_text(
        "change: CHANGE-001\nstatus: IN_PROGRESS\nbase_commit: 0000000\nreason: null\n\n"
        "# CHANGE-001\n\n## Semantic Diff\n\n### DECISIONS\n\n"
        f"{change_body}\n",
        encoding="utf-8",
    )
    return change


class MemoryReconciliationTests(unittest.TestCase):
    def test_affected_local_modify_and_remove(self) -> None:
        text = "**MODIFY D-003**\n**REMOVE R-004**\n**ADD R-A**"
        self.assertEqual(
            mod.affected_rdo_refs(text, "domain/example"),
            {"domain/example:D-003", "domain/example:R-004"},
        )

    def test_canonical_target_is_preserved(self) -> None:
        self.assertEqual(
            mod.affected_rdo_refs("**REMOVE other/domain:O-009**", "root"),
            {"other/domain:O-009"},
        )

    def test_add_only_does_not_create_inverse_impact(self) -> None:
        self.assertEqual(mod.affected_rdo_refs("**ADD D-A**", "root"), set())

    def test_promoted_finding_is_detected_after_modify(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            change = write_fixture(root, status="promoted", semantic_ref="root:D-001", change_body="- **MODIFY D-001** - nova redação")
            payload = mod.impacted_promoted_findings(root, change)
            self.assertEqual(payload["affected_rdo"], ["root:D-001"])
            self.assertEqual([item["finding"] for item in payload["impacted_promoted_findings"]], ["root:F-001"])

    def test_updated_reference_is_no_longer_stale_after_remove_add(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            change = write_fixture(
                root,
                status="promoted",
                semantic_ref="root:D-002",
                change_body="- **REMOVE D-001** - regra antiga\n- **ADD D-002** - regra substituta",
            )
            payload = mod.impacted_promoted_findings(root, change)
            self.assertEqual(payload["affected_rdo"], ["root:D-001"])
            self.assertEqual(payload["impacted_promoted_findings"], [])

    def test_reopened_active_finding_is_not_treated_as_stale_promoted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            change = write_fixture(root, status="active", semantic_ref="root:D-001", change_body="- **MODIFY D-001** - nova redação")
            payload = mod.impacted_promoted_findings(root, change)
            self.assertEqual(payload["impacted_promoted_findings"], [])

    def test_resolved_and_superseded_findings_are_not_treated_as_stale_promoted(self) -> None:
        for status in ("resolved", "superseded"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                change = write_fixture(root, status=status, semantic_ref="root:D-001", change_body="- **MODIFY D-001** - nova redação")
                payload = mod.impacted_promoted_findings(root, change)
                self.assertEqual(payload["impacted_promoted_findings"], [])

    def test_unrelated_promoted_finding_is_preserved_outside_impact_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            change = write_fixture(root, status="promoted", semantic_ref="root:D-001", change_body="- **MODIFY D-001** - nova redação")
            payload = mod.impacted_promoted_findings(root, change)
            ids = {item["finding"] for item in payload["impacted_promoted_findings"]}
            self.assertEqual(ids, {"root:F-001"})
            self.assertNotIn("root:F-002", ids)

    def test_semantic_ref_format_requires_canonical_rdo_identity(self) -> None:
        self.assertIsNotNone(CANONICAL_RDO_REF_RE.fullmatch("root:D-001"))
        self.assertIsNotNone(CANONICAL_RDO_REF_RE.fullmatch("domain/example:R-014"))
        self.assertIsNone(CANONICAL_RDO_REF_RE.fullmatch("D-001"))
        self.assertIsNone(CANONICAL_RDO_REF_RE.fullmatch("root:CHANGE-001"))

    def test_protocol_declares_all_approved_outcomes(self) -> None:
        spec = (ROOT / "SEMANTIC_GIT.md").read_text(encoding="utf-8")
        for token in (
            "permanecer `promoted`",
            "atualizar `semantic_refs`",
            "tornar-se `resolved`",
            "tornar-se `superseded`",
            "retornar a `active`",
        ):
            self.assertIn(token, spec)

    def test_protocol_preserves_unrelated_findings(self) -> None:
        spec = (ROOT / "SEMANTIC_GIT.md").read_text(encoding="utf-8")
        self.assertIn("Findings sem relação determinística", spec)
        self.assertIn("devem permanecer intactos", spec)

    def test_current_memory_surface_is_findings_only(self) -> None:
        spec = (ROOT / "SEMANTIC_GIT.md").read_text(encoding="utf-8")
        self.assertIn("`FINDINGS.yaml` é o único arquivo canônico permitido", spec)
        self.assertIn("exige evolução normativa explícita", spec)


if __name__ == "__main__":
    unittest.main()
