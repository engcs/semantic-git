#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _scripts._internal import memory_reconciliation as mod
from _scripts._internal.validate_structure import CANONICAL_RDO_REF_RE, Validator

ROOT = Path(__file__).resolve().parents[1]


def finding_yaml(*, estado: str = "promovido", ref: str = "root:D-001", abstraction: str = "0.7", include_risk: bool = False, include_sample: bool = True) -> str:
    risk = "\n    risco:\n      consequencia: exemplo opcional" if include_risk else ""
    sample = (
        "\n      amostras:\n"
        "        - tipo: implementacao\n"
        "          artefato: exemplo.sql\n"
        "          localizador: linhas 1-3\n"
        "          amostra: |\n"
        "            CASE WHEN A THEN 1 END"
        if include_sample
        else ""
    )
    return f"""esquema: semantic-git-achados-v2
espaco_semantico: root
autoridade: memoria_analitica_nao_autoritativa
nivel_abstracao: {abstraction}
achados:
  - id: F-001
    chave: exemplo.regra
    estado: {estado}
    tipo: fato_semantico
    aplica_se_a:
      versao_semantica: atual
    afirmacao: >
      Regra material reconstruída.
    evidencias:
      certeza: comprovada{sample}
    semantica:
      papel: regra
      estado: candidato
    rdo:
      disposicao: {estado}
      referencias:
        - {ref}{risk}
"""


def write_fixture(root: Path, *, estado: str, semantic_ref: str, change_body: str, include_unrelated: bool = True) -> Path:
    (root / "_changes").mkdir(parents=True)
    (root / "DECISIONS.md").write_text(
        "# Decisions - Root\n\n## Cabeçalho\n\nTeste.\n\n## Corpo\n\n"
        "- **D-001** - Regra original.\n"
        "- **D-002** - Regra substituta.\n",
        encoding="utf-8",
    )
    memory = root / "_memory"
    memory.mkdir()
    findings = finding_yaml(estado=estado, ref=semantic_ref).rstrip()
    if include_unrelated:
        findings += """
  - id: F-002
    chave: exemplo.regra_nao_relacionada
    estado: promovido
    tipo: contexto_historico
    aplica_se_a:
      versao_semantica: atual
    afirmacao: >
      Descoberta não relacionada.
    evidencias:
      certeza: comprovada
      amostras:
        - tipo: documento
          artefato: contexto.md
          localizador: seção 2
          amostra: >
            Evidência curta.
    semantica:
      papel: contexto
      estado: promovido
    rdo:
      disposicao: promovido
      referencias:
        - root:D-002
"""
    (memory / "FINDINGS.yaml").write_text(findings + "\n", encoding="utf-8")
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
        self.assertEqual(mod.affected_rdo_refs(text, "domain/example"), {"domain/example:D-003", "domain/example:R-004"})

    def test_add_only_does_not_create_inverse_impact(self) -> None:
        self.assertEqual(mod.affected_rdo_refs("**ADD D-A**", "root"), set())

    def test_promovido_finding_is_detected_after_modify(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            change = write_fixture(root, estado="promovido", semantic_ref="root:D-001", change_body="- **MODIFY D-001** - nova redação")
            payload = mod.impacted_promoted_findings(root, change)
            self.assertEqual(payload["affected_rdo"], ["root:D-001"])
            self.assertEqual([item["finding"] for item in payload["impacted_promoted_findings"]], ["root:F-001"])

    def test_ativo_finding_is_not_treated_as_stale_promoted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            change = write_fixture(root, estado="ativo", semantic_ref="root:D-001", change_body="- **MODIFY D-001** - nova redação")
            payload = mod.impacted_promoted_findings(root, change)
            self.assertEqual(payload["impacted_promoted_findings"], [])

    def test_unrelated_promoted_finding_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            change = write_fixture(root, estado="promovido", semantic_ref="root:D-001", change_body="- **MODIFY D-001** - nova redação")
            payload = mod.impacted_promoted_findings(root, change)
            ids = {item["finding"] for item in payload["impacted_promoted_findings"]}
            self.assertEqual(ids, {"root:F-001"})
            self.assertNotIn("root:F-002", ids)

    def test_reference_format_requires_canonical_rdo_identity(self) -> None:
        self.assertIsNotNone(CANONICAL_RDO_REF_RE.fullmatch("root:D-001"))
        self.assertIsNotNone(CANONICAL_RDO_REF_RE.fullmatch("domain/example:R-014"))
        self.assertIsNone(CANONICAL_RDO_REF_RE.fullmatch("D-001"))
        self.assertIsNone(CANONICAL_RDO_REF_RE.fullmatch("root:CHANGE-001"))

    def test_human_clarification_preserves_identity_and_unrelated(self) -> None:
        findings = [
            {
                "id": "F-001",
                "chave": "exemplo.regra",
                "estado": "ativo",
                "afirmacao": "interpretação anterior",
                "evidencias": {"certeza": "comprovada", "amostras": []},
                "semantica": {"estado": "nao_resolvido"},
                "rdo": {"disposicao": "revisao"},
            },
            {
                "id": "F-002",
                "chave": "exemplo.outra",
                "estado": "ativo",
                "afirmacao": "finding não relacionado",
                "evidencias": {"certeza": "comprovada", "amostras": []},
                "semantica": {"estado": "candidato"},
                "rdo": {"disposicao": "candidato"},
            },
        ]
        unrelated_before = findings[1].copy()
        result = mod.upsert_human_clarification(
            findings,
            "F-001",
            statement="entendimento corrigido pelo humano",
            human_provenance="clarificação humana durante investigação",
        )
        self.assertEqual([item["id"] for item in result["findings"]], ["F-001", "F-002"])
        self.assertEqual(result["findings"][1], unrelated_before)
        self.assertEqual(result["findings"][0]["afirmacao"], "entendimento corrigido pelo humano")
        self.assertIn(
            {
                "tipo": "clarificacao_humana",
                "fonte": "humano",
                "localizador": "clarificação humana durante investigação",
                "amostra": "entendimento corrigido pelo humano",
            },
            result["findings"][0]["evidencias"]["amostras"],
        )

    def test_human_uncertainty_reopens_promoted_finding(self) -> None:
        findings = [
            {
                "id": "F-001",
                "chave": "exemplo.regra",
                "estado": "promovido",
                "afirmacao": "regra promovida",
                "evidencias": {"certeza": "comprovada", "amostras": []},
                "semantica": {"estado": "promovido"},
                "rdo": {"disposicao": "promovido", "referencias": ["root:D-001"]},
            }
        ]
        result = mod.upsert_human_clarification(
            findings,
            "F-001",
            statement="o humano indicou interpretação concorrente",
            human_provenance="clarificação humana com ressalva",
            uncertain=True,
            potential_rdo_conflict=True,
        )
        finding = result["findings"][0]
        self.assertEqual(finding["estado"], "ativo")
        self.assertEqual(finding["semantica"]["estado"], "nao_resolvido")
        self.assertEqual(finding["rdo"]["referencias"], ["root:D-001"])
        self.assertEqual(finding["rdo"]["disposicao"], "revisao")
        self.assertTrue(result["review_required"])
        self.assertTrue(result["rdo_reconciliation_required"])


class FindingsV2StructuralTests(unittest.TestCase):
    def validator(self, root: Path) -> Validator:
        spec = root / "SEMANTIC_GIT.md"
        spec.write_text("# spec\n", encoding="utf-8")
        validator = Validator(root, spec)
        (root / "DECISIONS.md").write_text(
            "# Decisions - Root\n\n## Cabeçalho\n\nTeste.\n\n## Corpo\n\n- **D-001** - Regra.\n",
            encoding="utf-8",
        )
        validator.validate_rdo(root / "DECISIONS.md")
        return validator

    def write_memory(self, root: Path, text: str) -> Path:
        memory = root / "_memory"
        memory.mkdir()
        path = memory / "FINDINGS.yaml"
        path.write_text(text, encoding="utf-8")
        return path

    def test_risk_is_optional_and_ptbr_schema_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            validator = self.validator(root)
            validator.validate_memory_file(self.write_memory(root, finding_yaml(include_risk=False)))
            self.assertEqual(validator.findings, [])

    def test_abstraction_must_use_tenths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            validator = self.validator(root)
            validator.validate_memory_file(self.write_memory(root, finding_yaml(abstraction="0.75")))
            self.assertTrue(any(item["rule"] == "MEMORY_ABSTRACTION" for item in validator.findings))

    def test_material_finding_requires_verifiable_sample(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            validator = self.validator(root)
            validator.validate_memory_file(self.write_memory(root, finding_yaml(include_sample=False)))
            self.assertTrue(any(item["rule"] == "MEMORY_EVIDENCE" for item in validator.findings))

    def test_orphan_promoted_reference_fails_canonical_validator(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            validator = self.validator(root)
            validator.validate_memory_file(self.write_memory(root, finding_yaml(ref="root:D-999")))
            self.assertTrue(any(item["rule"] == "MEMORY_SEMANTIC_REF_ENDPOINT" for item in validator.findings))

    def test_protocol_declares_native_current_state_memory(self) -> None:
        spec = (ROOT / "SEMANTIC_GIT.md").read_text(encoding="utf-8")
        for token in (
            "componente nativo do Semantic Git",
            "estado atual do conhecimento",
            "nivel_abstracao",
            "NAO_SUSTENTADO",
            "Git",
        ):
            self.assertIn(token, spec)

    def test_memory_skill_declares_no_embedded_version_history(self) -> None:
        skill = (ROOT / ".opencode/skills/semantic-memory/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("estado atual do conhecimento", skill)
        self.assertIn("após V19", skill)
        self.assertIn("Git é suficiente", skill)
        self.assertIn("não autoritativo perante R/D/O", skill)


if __name__ == "__main__":
    unittest.main()
