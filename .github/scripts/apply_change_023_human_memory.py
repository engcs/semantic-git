from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


# Normative protocol
p = Path("SEMANTIC_GIT.md")
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    "### 32.10. Publicação",
    """### 32.10. Correções e complementos humanos

Uma correção, complemento, ressalva ou esclarecimento material fornecido pelo humano durante uma investigação pode constituir nova evidência analítica e deve ser preservado quando satisfizer os critérios de retenção desta seção. A interação, por si só, não transforma a afirmação em verdade semântica autoritativa nem autoriza alteração direta de R/D/O.

Antes de criar novo finding para uma correção humana, a IA deve procurar finding semanticamente equivalente na memória aplicável. Quando a questão analítica continuar sendo a mesma, deve preservar o mesmo `F-*` e reconciliar o finding existente por upsert. Mudança de redação, aumento de precisão, complemento ou correção do entendimento não cria nova identidade por si só. Novo `F-*` somente é apropriado quando o achado ou a questão analítica for materialmente distinta.

A retenção deve registrar somente a síntese material do que foi esclarecido e proveniência humana suficiente para compreender a origem da correção. Não armazenar transcrição integral da conversa, chain-of-thought, raciocínio interno ou dump da interação. A evidência anterior e findings não relacionados permanecem intactos salvo quando a própria correção fornecer base material para alterá-los.

A correção humana pode justificar mudança de certeza, risco, classificação ou `semantic_status` somente na medida sustentada pelo esclarecimento efetivamente fornecido. Ela não deve converter silenciosamente hipótese, ressalva, conflito ou dúvida em certeza. Quando permanecer mais de uma interpretação material plausível, o finding deve continuar não resolvido e a decisão dependente deve produzir `REVIEW`.

O fluxo conceitual é:

```text
correção / complemento humano
→ localizar memória e finding equivalente
→ preservar F-* quando a identidade analítica permanece
→ sintetizar a correção + registrar proveniência humana
→ preservar incerteza material quando existir
→ atualizar apenas o finding afetado
```

Se o humano declarar que o entendimento deve tornar-se regra autoritativa, essa declaração pode motivar promoção, mas não substitui governança:

```text
clarificação humana
→ memória analítica, quando aplicável
→ CHANGE aplicável
→ revisão semântica
→ aprovação humana
→ R/D/O
```

Nenhuma declaração conversacional, por mais explícita que seja sobre o conteúdo do domínio, autoriza pular CHANGE, gates ou incorporação quando a alteração de R/D/O for material.

Quando a correção atingir finding com `status: promoted` e puder tornar sua relação com o R/D/O vigente incompatível, a questão analítica deve ser reaberta e reconciliada. Conforme o significado observado, o finding pode retornar a `active` com `semantic_status` não resolvido, preservando a proveniência e as referências necessárias para localizar a autoridade afetada. Enquanto a incompatibilidade material não estiver resolvida, conclusões ou promoções que dependam dessa relação permanecem em `REVIEW` e o R/D/O não deve ser alterado silenciosamente.

### 32.11. Publicação""",
    "human clarification section",
)
s = replace_once(s, "### 32.11. Validação estrutural", "### 32.12. Validação estrutural", "memory validation numbering")
s = replace_once(s, "### 32.12. Invariantes da memória analítica", "### 32.13. Invariantes da memória analítica", "memory invariants numbering")
s = replace_once(
    s,
    "19. Findings não relacionados à alteração devem permanecer intactos.",
    """19. Findings não relacionados à alteração devem permanecer intactos.
20. Correção ou complemento humano material pode ser preservado como evidência analítica sem se tornar autoridade semântica apenas por ter sido declarado na interação.
21. Correção humana da mesma questão analítica preserva o mesmo `F-*`; novo ID exige achado materialmente distinto.
22. Incerteza, ressalva ou interpretação concorrente expressa pelo humano permanece explicitamente não resolvida quando material e produz `REVIEW` quando uma decisão depender dela.
23. Intenção humana de tornar um entendimento autoritativo não contorna CHANGE, revisão, aprovação ou incorporação em R/D/O.
24. Memória de correção humana preserva síntese material e proveniência suficiente, nunca transcrição integral da conversa ou raciocínio interno.""",
    "human clarification invariants",
)
p.write_text(s, encoding="utf-8")


# Semantic-memory skill
p = Path(".opencode/skills/semantic-memory/SKILL.md")
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    "## 7. Lifecycle states",
    """## 6.1. Human corrections and complements

Treat a material human correction, complement or caveat as analytical evidence, not as automatic semantic authority.

Operational flow:

```text
human clarification
-> inspect relevant FINDINGS.yaml
-> search for a semantically equivalent finding
-> same analytical identity: upsert the same F-*
-> distinct analytical issue: allocate a new F-* only if it passes retention
-> record a concise human-provenance locator
-> preserve uncertainty and unrelated findings
```

When upserting the same finding:

- preserve its `F-*` identity;
- update only meaning actually clarified by the human;
- do not upgrade certainty, risk or semantic status beyond what the clarification supports;
- preserve findings outside the clarified issue;
- store the material synthesis, not the chat transcript;
- never store chain-of-thought or internal reasoning.

If the human expresses doubt, a hypothesis, a condition or competing interpretations, keep the material issue unresolved. Use `REVIEW` when a later decision or promotion depends on choosing among those interpretations.

If the human explicitly says the clarification should become an authoritative domain rule, retain the analytical clarification when useful but route semantic promotion through the applicable CHANGE and normal approval gates. Do not edit R/D/O merely because the statement was authoritative in tone.

If the correction concerns a `promoted` finding and may conflict with its `semantic_refs`, reopen the analytical question, normally returning the finding to `active`/unresolved until the relationship is reconciled. Preserve enough provenance and reference information to identify the affected authority. Do not silently rewrite R/D/O.

Deterministic tooling may enforce preservation of IDs, unrelated findings, concise provenance, unresolved status and promotion/reconciliation flags after the agent has semantically identified which existing finding the human clarification concerns. Semantic equivalence itself remains an interpretive judgment and must produce `REVIEW` when materially ambiguous.

## 7. Lifecycle states""",
    "skill human clarification flow",
)
p.write_text(s, encoding="utf-8")


# Deterministic helper for an already-resolved finding identity
p = Path("_scripts/_internal/memory_reconciliation.py")
s = p.read_text(encoding="utf-8")
s = replace_once(s, "import argparse\nimport json\nimport re", "import argparse\nfrom copy import deepcopy\nimport json\nimport re", "memory helper import")
helper = r'''

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
'''
s = replace_once(s, "\ndef main() -> int:\n", helper + "\n\ndef main() -> int:\n", "human clarification helper")
p.write_text(s, encoding="utf-8")


# Tests
p = Path("_scripts/test_memory_reconciliation.py")
s = p.read_text(encoding="utf-8")
tests = r'''
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
'''
s = replace_once(s, "\n\nif __name__ == \"__main__\":\n", "\n" + tests + "\n\nif __name__ == \"__main__\":\n", "human clarification tests")
p.write_text(s, encoding="utf-8")
