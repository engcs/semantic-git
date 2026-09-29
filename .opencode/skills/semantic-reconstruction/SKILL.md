---
name: semantic-reconstruction
description: Use when durable business meaning must be reverse-engineered from an existing or legacy implementation. Reconstructs behavioral closure, UPSERTs the minimum reconstructable FINDINGS knowledge set, isolates semantic versions, and produces evidence-backed candidate R/D/O for governed review.
compatibility: Semantic Git 1.5
---

# Semantic Reconstruction

Reconstruct the smallest complete semantic contract capable of reproducing the business behavior of an existing implementation without depending on its current physical form.

This skill derives all normative authority from `SEMANTIC_GIT.md`.

Central rule:

```text
compress implementation
not behavior
```

FINDINGS is a native Semantic Git capability used transversally by reconstruction. Its content is analytical and non-authoritative relative to R/D/O, but reconstruction must use its normative lifecycle, evidence, abstraction and reconciliation rules.

## 1. Objective

Recover durable business meaning with enough completeness that another capable agent can:

- understand the subject;
- reconstruct candidate R/D/O;
- reimplement the behavior without inventing business rules;
- verify later R/D/O edits against the discoveries already made;
- identify what remains uncertain without repeating the whole investigation.

The goal is not to describe code and not to preserve a transcript of investigation.

## 2. Establish the semantic target

Before deep physical analysis:

- identify the target Semantic Namespace;
- read applicable ancestral Requirements;
- read relevant Decisions and Operations;
- identify the semantic subject;
- identify the target semantic version or current behavior when versions exist;
- identify explicit evidence boundaries from the human;
- load relevant current FINDINGS when they may affect reconstruction, known edge cases or version boundaries.

FINDINGS is context and discovered knowledge, not automatic authority. Material claims should still be traceable to evidence, an applicable ancestor or a governed human decision.

## 3. Semantic version is not Git chronology

Never assume:

```text
first commit = first semantic version
later commit = later semantic rule
```

Semantic version is behavioral identity.

A later physical artifact may still materialize an earlier semantic version. One semantic version may span many physical revisions.

When the task isolates V1, do not borrow a V2-only rule. When V2 is investigated after V1, compare new evidence to the current knowledge state rather than rebuilding an embedded historical encyclopedia.

## 4. Build behavioral closure

Do not stop at one target file. Follow all dependencies required to recover behavior, including as applicable:

- upstream transformations;
- downstream calculations;
- shared models and macros;
- status mappings;
- calendars;
- eligibility;
- temporal windows;
- exclusions;
- aggregation;
- formulas;
- version-neutral shared behavior.

Investigation is complete when the semantic core can be stated without implementation vocabulary or when material evidence is genuinely unavailable.

## 5. Keep products conceptually separate

### Evidence map

Working structure containing physical source, relevant fragment, semantic interpretation, applicability, confidence, conflicts and inheritance.

It may be temporary.

### Behavioral semantic model

Working understanding of:

- purpose;
- elementary fact;
- population;
- components/measures/states;
- contribution/classification;
- time;
- recuts;
- aggregation;
- formulas;
- edge cases;
- relationships.

### FINDINGS

Persistent analytical memory containing the **minimum structured set of material discoveries necessary to reconstruct and verify the current understanding later**.

This is broader than exceptions and risks. Positive discoveries such as purpose, component definitions, formulas and invariants belong when needed for reconstructibility.

Do not copy the evidence map into `_memory`. Convert evidence into semantic findings with:

- stable identity;
- concise `afirmacao`;
- applicability;
- evidence samples;
- semantic role;
- R/D/O disposition.

### Candidate R/D/O

Authoritative only after normal Semantic Git governance. Draft from the reconstructed essence, not by mechanically mapping one finding to one R/D/O item.

### Review package

Preserve enough evidence, findings, classifications and unresolved questions for conceptual/mathematical review without restarting blindly.

## 6. Semantic core

Before drafting R/D/O, answer or explicitly leave in REVIEW:

### Purpose
What business question does the subject answer?

### Elementary fact
What independently classified or measured occurrence exists?

### Population
Which occurrences are eligible? What boundaries matter?

### Components / measures / states
What semantic components independently contribute to the result?

### Contribution/classification
Under what conditions does each eligible occurrence contribute or change state?

### Time
Which date/event situates the occurrence? What competence, validity and timeliness rules apply?

### Recuts
Which views/segments alter participation or publication?

### Aggregation
How do elementary contributions become published results?

### Formula
What mathematical relation expresses the metric using the most human-readable semantic components?

### Edge cases
What happens for zero denominator, nulls, cancellations, expurgos and other material boundaries?

### Versions and applicability
Which truths are current, which variants still materially govern current reality, and which historical states belong only to Git?

## 7. Mathematical closure

If quantitative behavior is material, verify as applicable:

- admissible domain;
- division by zero / 0÷0;
- piecewise totality;
- overlap/uniqueness;
- exact boundaries;
- aggregation order;
- rounding/truncation;
- units/dimensions;
- invariants.

Keep separate:

```text
mathematical behavior
physical engine behavior
semantic convention
```

Do not turn engine fallback into semantic convention without evidence or governed human decision.

## 8. Deterministic interpretation vs invention

Synthesis is allowed when multiple physical conditions deterministically compose one business rule and:

1. dependencies were inspected;
2. physical behavior is unambiguous;
3. no materially competing interpretation remains;
4. no unsupported intent/motivation is invented.

If behavior is proven but meaning remains unclear, preserve the narrower finding and uncertainty; do not force a human-sounding rule.

## 9. Inheritance subtraction

After reconstructing complete behavior, classify knowledge as:

- inherited from ancestor;
- common and better placed in ancestor;
- local;
- another consumer;
- another semantic version;
- physical-only;
- unresolved;
- material analytical finding.

Do not duplicate inherited R/D/O locally.

FINDINGS may still preserve local evidence and discovery when needed to verify/reconstruct the local subject, but it must not create a competing semantic authority.

## 10. Materialize FINDINGS by UPSERT

Before writing candidate R/D/O, reconcile the current investigation against existing FINDINGS.

For each material discovery:

```text
same identity + same truth
→ same F-*; enrich evidence

same identity + better evidence
→ same F-*; update certainty/amostras

same identity + physical refactor only
→ same semantics; update evidence locator if useful

same identity + material semantic change
→ update current knowledge; Git preserves prior state
→ if prior rule still governs current reality, preserve explicit applicable variant

materially incompatible evidence
→ drift/REVIEW; never silent overwrite

new material identity
→ new F-*
```

Do not delete an existing finding merely because the current pass did not rediscover it.

## 11. Evidence samples

Each material finding should include a short human-verifiable sample:

```yaml
evidencias:
  certeza: comprovada
  amostras:
    - tipo: implementacao
      artefato: model.sql
      localizador: linhas 120-135
      amostra: |
        CASE ... END
```

Prefer the smallest fragment that lets a human see why the statement is plausible and reopen the original source.

For mathematical findings, a witness/expression/test result can be the sample.

Do not dump long source content.

## 12. Abstraction control

Use requested `nivel_abstracao` from `0.0` to `1.0` in steps of `0.1`; default to `0.7`.

- `0.0`: granular discoveries and more physical evidence, without chain-of-thought.
- `0.7`: balanced reconstructibility/auditability/context cost.
- `1.0`: strongest semantic synthesis, accepting explicit loss of fine implementation detail.

All levels must preserve the same evidence-supported truth and material uncertainty. Abstraction is compression, not permission to simplify away contradictions.

## 13. Evolution across versions

When investigating V2 with V1 knowledge available, ask:

> What does V2 force us to change in what we currently know?

Do not ask only “what exists in V2?”.

For each current proposition:

```text
V2 confirms
→ keep finding, optionally enrich evidence

V2 refines without semantic change
→ UPSERT same finding

V2 changes only implementation
→ keep semantic finding

V2 changes meaning
→ update current finding / applicability
→ evaluate CHANGE for R/D/O

V2 cannot verify
→ do not extrapolate applicability

V2 introduces new knowledge
→ new finding
```

Do not embed V1→V2→…→V19 genealogy in current FINDINGS by default. Git owns that history.

Historical variants remain materialized only while needed for current interpretation, replay, audit, coexistence or another current responsibility.

## 14. Requirements

Requirements express stable truths, necessities and invariants.

They may contain:

- purpose;
- population;
- semantic meaning of components;
- material invariants;
- required recuts;
- **the defining human-readable formula of a calculable indicator when that formula directly expresses what the indicator means**.

For example, a Requirement may express:

```text
EXEC_PROG = EXECUTADO / PROGRAMADO
```

when EXECUTADO and PROGRAMADO are semantic components.

Do not put table/column/model names or physical aliases in Requirements.

## 15. Decisions

Decisions define durable conceptual choices needed to satisfy Requirements, including:

- component definitions;
- eligibility;
- status semantics;
- calendar conventions;
- aggregation order;
- zero-denominator behavior;
- precision conventions;
- temporal interpretations;
- edge-case semantics.

When a Requirement carries the defining metric formula, Decisions explain the components and conventions. Do not demote the main formula into physical vocabulary.

## 16. Operations

Operations describe reconstructible behavior/materialization without becoming implementation inventory.

Prefer conceptual sequence:

```text
elementary fact
→ context
→ eligibility
→ classification/contribution
→ exclusions
→ aggregation
→ formula/outcome
→ consolidation/publication
```

Physical names may appear when they are necessary to describe actual materialization and remain supported by the protocol’s R/D/O separation.

Operations must not invent semantic rules absent from Requirements/Decisions.

## 17. RDO reconstruction audit

After drafting R/D/O, verify both directions.

### FINDINGS → RDO

For every material applicable finding, determine disposition:

- promoted/represented;
- partially represented;
- inherited;
- intentionally non-semantic;
- review;
- not promoted with reason.

No material discovery should silently disappear.

### RDO → FINDINGS

For every material proposition in new/edited R/D/O, locate support from:

- FINDINGS;
- applicable ancestor;
- governed human decision.

Classify:

```text
SUSTENTADO
PARCIAL
CONTRADITO
NAO_SUSTENTADO
AMBIGUO
EVIDENCIA_DESATUALIZADA
```

Do not treat absence of evidence as contradiction.

## 18. Directed reinvestigation

If R/D/O proposition is `NAO_SUSTENTADO` or `CONTRADITO`, a directed investigation can test it.

Search for:

- confirming evidence;
- refuting evidence;
- competing interpretations.

UPSERT new discoveries, then re-run the audit.

If support still does not exist, keep the proposition in REVIEW/non-supported rather than accepting it by silence.

A deliberate TO-BE may legitimately differ from current findings, but must be governed by CHANGE and human approval.

## 19. Reconstruction test

Ask:

> If implementation disappeared and another engineer received applicable ancestors + current FINDINGS + approved R/D/O, could they understand and reproduce the intended behavior without inventing material business rules?

If no, recover missing knowledge or make the limitation explicit.

## 20. Reimplementation test

Ask:

> If SQL, dbt, database, field names and physical architecture changed completely, would this semantic contract remain true?

If no, the contract is too physical.

A physical fact that fails this test can still belong in FINDINGS when it is necessary for verification/reconstruction or captures unresolved material behavior.

## 21. REVIEW is a last resort

Do not use REVIEW merely because meaning is distributed or encoded in flags.

Before REVIEW:

1. follow dependencies;
2. resolve mappings;
3. inspect conditions;
4. combine same-rule behavior;
5. isolate semantic-version applicability;
6. translate behavior to domain concepts;
7. test competing interpretations.

```text
unknown because not investigated
!= REVIEW

unknown after relevant evidence exhausted
= REVIEW
```

## 22. Final checklist

Before completion:

- behavioral closure is sufficient;
- semantic target/version is isolated;
- evidence samples exist for material findings;
- FINDINGS was UPSERTed instead of blindly appended/replaced;
- positive reconstructive knowledge was not discarded because it lacked risk;
- historical genealogy was not embedded unnecessarily;
- abstraction level is explicit and respected;
- defining indicator formula uses semantic components at the highest appropriate R/D/O level;
- every material finding has R/D/O disposition;
- every material R/D/O proposition has support, ancestor, governed decision or visible REVIEW;
- contradictions and unsupported claims are distinct;
- no chain-of-thought or investigation transcript was persisted;
- R/D/O remains the only authoritative semantic contract.
