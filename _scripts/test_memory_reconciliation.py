#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

from _scripts._internal import memory_reconciliation as mod

ROOT = Path(__file__).resolve().parents[1]


class MemoryReconciliationTests(unittest.TestCase):
    def test_affected_local_modify_and_remove(self) -> None:
        text = "**MODIFY D-003**\n**REMOVE R-004**\n**ADD R-A**"
        self.assertEqual(mod.affected_rdo_refs(text, "domain/example"), {"domain/example:D-003", "domain/example:R-004"})

    def test_canonical_target_is_preserved(self) -> None:
        self.assertEqual(mod.affected_rdo_refs("**REMOVE other/domain:O-009**", "root"), {"other/domain:O-009"})

    def test_add_only_does_not_create_inverse_impact(self) -> None:
        self.assertEqual(mod.affected_rdo_refs("**ADD D-A**", "root"), set())

    def test_protocol_declares_all_approved_outcomes(self) -> None:
        spec = (ROOT / "SEMANTIC_GIT.md").read_text(encoding="utf-8")
        for token in ("permanecer `promoted`", "atualizar `semantic_refs`", "tornar-se `resolved`", "tornar-se `superseded`", "retornar a `active`"):
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
