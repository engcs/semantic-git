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


    def test_human_clarification_preserves_finding_identity_and_unrelated(self) -> None:
        findings = [
            {
                "id": "F-001",
                "status": "active",
                "summary": "interpretação anterior",
                "evidence": {"certainty": "proven", "sources": []},
                "semantic_status": {"state": "unresolved", "reason": "aguarda esclarecimento"},
            },
            {
                "id": "F-002",
                "status": "active",
                "summary": "finding não relacionado",
                "evidence": {"certainty": "proven"},
                "semantic_status": {"state": "non_semantic"},
            },
        ]
        unrelated_before = findings[1].copy()
        result = mod.upsert_human_clarification(
            findings,
            "F-001",
            summary="entendimento corrigido pelo humano",
            human_provenance="clarificação humana durante investigação",
        )
        self.assertEqual([item["id"] for item in result["findings"]], ["F-001", "F-002"])
        self.assertEqual(result["finding_id"], "F-001")
        self.assertEqual(result["findings"][1], unrelated_before)
        self.assertEqual(result["findings"][0]["evidence"]["certainty"], "proven")
        self.assertIn(
            {"type": "human_clarification", "locator": "clarificação humana durante investigação"},
            result["findings"][0]["evidence"]["sources"],
        )

    def test_human_uncertainty_reopens_promoted_finding_and_requires_review(self) -> None:
        findings = [
            {
                "id": "F-001",
                "status": "promoted",
                "summary": "regra promovida",
                "evidence": {"certainty": "proven", "sources": []},
                "semantic_status": {"state": "promoted", "reason": "promovido"},
                "semantic_refs": ["root:D-001"],
            }
        ]
        result = mod.upsert_human_clarification(
            findings,
            "F-001",
            summary="o humano indicou uma interpretação concorrente",
            human_provenance="clarificação humana com ressalva",
            uncertain=True,
            potential_rdo_conflict=True,
        )
        finding = result["findings"][0]
        self.assertEqual(finding["id"], "F-001")
        self.assertEqual(finding["status"], "active")
        self.assertEqual(finding["semantic_status"]["state"], "unresolved")
        self.assertEqual(finding["semantic_refs"], ["root:D-001"])
        self.assertTrue(result["review_required"])
        self.assertTrue(result["rdo_reconciliation_required"])

    def test_human_normative_intent_requires_change_without_auto_promotion(self) -> None:
        findings = [
            {
                "id": "F-001",
                "status": "active",
                "summary": "achado",
                "evidence": {"certainty": "proven", "sources": []},
                "semantic_status": {"state": "candidate", "reason": "candidato"},
            }
        ]
        result = mod.upsert_human_clarification(
            findings,
            "F-001",
            summary="o humano declarou que o entendimento deve ser autoritativo",
            human_provenance="declaração humana de intenção normativa",
            normative_intent=True,
        )
        self.assertTrue(result["promotion_requires_change"])
        self.assertEqual(result["findings"][0]["status"], "active")
        self.assertEqual(result["findings"][0]["semantic_status"]["state"], "candidate")

    def test_human_provenance_rejects_transcript_sized_input(self) -> None:
        findings = [
            {
                "id": "F-001",
                "status": "active",
                "summary": "achado",
                "evidence": {"sources": []},
                "semantic_status": {"state": "unresolved"},
            }
        ]
        with self.assertRaisesRegex(ValueError, "material synthesis, not a transcript"):
            mod.upsert_human_clarification(
                findings,
                "F-001",
                summary="síntese válida",
                human_provenance="x" * 401,
            )

    def test_protocol_declares_human_clarification_contract(self) -> None:
        spec = (ROOT / "SEMANTIC_GIT.md").read_text(encoding="utf-8")
        for token in (
            "Correções e complementos humanos",
            "preservar o mesmo `F-*`",
            "não transforma a afirmação em verdade semântica autoritativa",
            "Não armazenar transcrição integral da conversa",
            "não substitui governança",
        ):
            self.assertIn(token, spec)

    def test_skill_declares_human_clarification_flow(self) -> None:
        skill = (ROOT / ".opencode/skills/semantic-memory/SKILL.md").read_text(encoding="utf-8")
        for token in (
            "Human corrections and complements",
            "upsert the same F-*",
            "store the material synthesis, not the chat transcript",
            "route semantic promotion through the applicable CHANGE",
            "Semantic equivalence itself remains an interpretive judgment",
        ):
            self.assertIn(token, skill)


if __name__ == "__main__":
    unittest.main()
