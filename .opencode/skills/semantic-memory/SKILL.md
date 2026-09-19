---
name: semantic-memory
description: Use to read, create, reconcile or update a Semantic Namespace analytical memory in _memory/FINDINGS.yaml. Preserves material findings, exceptions, risks, unresolved meaning, mathematical gaps and evidence that are costly or dangerous to rediscover but are not authoritative R/D/O. This skill is transversal and does not replace Semantic Git governance.
compatibility: Semantic Git 1.5
---

# Semantic Memory

Manage the analytical memory of a Semantic Namespace without turning analysis into semantic authority.

This skill derives all normative authority from `SEMANTIC_GIT.md`. It is a transversal capability used by `semantic-extraction`, `semantic-reconstruction`, `semantic-conceptual-review`, `semantic-mathematical-review`, reimplementation, risk analysis and debugging when analytical findings must survive beyond one session.

## Fundamental distinction

```text
R/D/O
= what is semantically authoritative now

_memory/FINDINGS.yaml
= what is important not to forget

Git / source implementation
= original physical evidence
```

Treat R/D/O and active analytical memory as separate current-state responsibilities. A finding that is already adequately represented as authoritative R/D/O should not remain duplicated as an active memory rule. Conversely, a finding that remains only in `_memory` must not be treated as normative input to R/D/O or implementation.

Promotion is the lifecycle bridge, not permission for two sources of truth. After approved promotion, R/D/O owns the current semantic rule; memory may retain the finding as `promoted` only to preserve analytical provenance, prior uncertainty, evidence/risk history and `semantic_refs` to the authoritative semantic item.

A finding can be true and materially important without being a durable domain rule.

Typical example:

```text
an implementation contains one hardcoded competence-specific exception
+
its behavioral effect is proven
+
its durable business meaning is unknown
```

Do not force that observation into R/D/O and do not discard it. Preserve it as analytical memory when the retention criteria are met.

The same principle applies to mathematical analysis. A proven indetermination, contradiction, boundary gap or quantitative divergence may be materially important even when it does not itself define the business rule.

## 1. Location and scope

Memory is local to the Semantic Namespace that owns the finding:

```text
<namespace>/
├── REQUIREMENTS.md
├── DECISIONS.md
├── OPERATIONS.md
├── _changes/
├── _publications/
└── _memory/
    └── FINDINGS.yaml
```

`_memory/`:

- does not create a Semantic Namespace;
- is not R/D/O;
- is not inherited automatically by descendants;
- is not a CHANGE;
- is not publication input by default;
- is versioned by Git;
- must not exist merely to complete directory structure.

Create `_memory/FINDINGS.yaml` only when at least one material finding qualifies for retention.

### Analytical writes while a CHANGE is DRAFT

Analytical memory is not semantic implementation. When a finding is discovered during an authorized investigation, creation or upsert of the applicable namespace's `_memory/FINDINGS.yaml` may occur while the related CHANGE is still `DRAFT`.

This permission is deliberately narrow:

- the write must be limited to non-authoritative analytical memory;
- the finding must satisfy the retention and evidence gates in this skill;
- it must arise from the investigation currently being performed;
- it must not alter R/D/O, `SEMANTIC_GIT.md`, implementation code, configuration, tests or other physical materialization;
- it must not be used to persist a semantic rule while avoiding approval;
- updating memory alone does not require a separate semantic CHANGE.

If the finding becomes a proposed durable semantic rule, stop treating promotion as a memory-only write and use the normal CHANGE and human-approval flow.

## 2. Retention test

Retain a finding when all of the following are true or materially applicable:

1. **Materiality** — forgetting it could alter interpretation, reproduction, risk assessment or investigation.
2. **Evidence** — it is observed directly or is an inference with explicit supporting evidence.
3. **Rediscovery cost or risk** — recovering it later would require meaningful investigation or its omission could cause a material mistake.
4. **Non-authoritative fit** — it does not currently belong in authoritative R/D/O, or its semantic meaning remains unresolved.

Good candidates include:

- hardcoded physical exceptions;
- implementation behavior whose business meaning is unresolved;
- known reimplementation hazards;
- evidence gaps that materially limit reconstruction;
- historical artifacts that explain otherwise surprising behavior;
- cross-version observations that must not contaminate the target semantic version;
- physical constraints that are important to preserve but not yet justified as domain rules;
- mathematical indeterminations or contradictions with a concrete witness;
- material boundary gaps or overlaps;
- aggregation-order or precision ambiguity capable of changing the result;
- dimensional inconsistencies;
- materialization behavior that contradicts a mathematical convention already governed by R/D/O.

Do not retain merely because something was observed.

## 3. What must not become memory

Do not use `_memory` as:

- chain-of-thought storage;
- transcript or session log;
- complete evidence-map dump;
- list of every file, JOIN, field or condition inspected;
- TODO list;
- duplicate of R/D/O;
- duplicate of CHANGE history;
- substitute for original source evidence;
- hidden place to persist a semantic rule without governance;
- dump of every mathematical check that passed;
- separate mathematical specification.

A finding with `status: active` must not simply restate knowledge already adequately represented in authoritative R/D/O. If a finding becomes authoritative through promotion, move semantic ownership to R/D/O and keep the memory record only as non-authoritative provenance with `status: promoted` and semantic references when useful.

A useful test is:

> Would a future investigator materially benefit from knowing this before reopening the original evidence?

If no, do not retain it.

## 4. Canonical file shape

`FINDINGS.yaml` represents the current analytical memory of the namespace.

Minimum shape:

```yaml
namespace: domain/example
findings:
  - id: F-001
    status: active
    category: physical_exception
    summary: >
      A concise statement of the material observation.
    evidence:
      certainty: proven
      sources:
        - repository: optional-repository-identity
          commit: optional-commit
          path: optional/path
          locator: optional human-readable locator
    risk:
      level: high
      consequence: >
        What can go wrong if the finding is forgotten or ignored.
    semantic_status:
      state: unresolved
      reason: >
        Why this is not authoritative semantic knowledge now.
```

Required finding fields are:

```text
id
status
category
summary
evidence
risk
semantic_status
```

Additional fields may be used when they improve provenance or lifecycle tracking, for example:

```yaml
discovered_by:
  - semantic-reconstruction
reviewed_by:
  - semantic-conceptual-review
semantic_refs:
  - domain/example:D-007
superseded_by: F-014
```

### Optional mathematical structure

A mathematical finding remains a normal `F-*` finding. Do not create a separate `MATHEMATICS.yaml` merely because its evidence is quantitative.

Use a category that makes the mathematical nature explicit, for example:

```text
mathematical_indeterminacy
mathematical_contradiction
mathematical_boundary_gap
mathematical_overlap
mathematical_aggregation_order
mathematical_precision
mathematical_dimension
```

When machine-readable detail is useful, add an optional `mathematics:` block. It may contain only the fields supported by the investigation, for example:

```yaml
mathematics:
  expression: "100 * executado / programado"
  domain_condition: "programado = 0"
  witness:
    executado: 0
    programado: 0
  semantic_expected:
    kpi: 0
  observed:
    kpi: null
  classification: contradiction
```

The block may also record proof, interval, boundary, units, aggregation order or precision convention when those are the material evidence. Do not force empty subfields.

`mathematics:` is analytical structure only. It does not create a mathematical source of truth parallel to R/D/O. If the authoritative rule already lives in R/D/O, the finding should preserve the inconsistency, witness, risk and provenance rather than duplicate the rule as an active semantic proposition.

Do not fabricate source paths, commits, certainty, rationale, mathematical domain or human intent.

## 5. Finding identity

Use local stable IDs:

```text
F-001
F-002
F-003
```

Rules:

- IDs are local to one namespace memory;
- one ID identifies one continuing analytical finding;
- do not renumber existing findings for convenience;
- do not create a new ID merely because wording changed;
- do not treat `F-*` as Semantic Git R/D/O identity;
- do not use a finding as a normative cross-namespace dependency.

Before creating a new ID, search existing findings for semantic equivalence.

For mathematical findings, a new witness for the same underlying gap normally enriches the existing finding rather than allocating another ID.

## 6. Upsert, never blind append or blind replace

The file represents **current analytical state**. Git preserves its historical states.

Therefore:

```text
new observation
-> search for equivalent finding
-> update existing finding when identity is preserved
-> create new F-* only when the finding is genuinely distinct
```

Never append a fresh copy of every result after each skill execution.

Never replace the whole memory from only the current execution's observations. Failure to rediscover an existing finding is not evidence that it became false or irrelevant.

When reprocessing memory:

- preserve findings not examined by the current task;
- enrich evidence when independently reobserved;
- update certainty only when evidence supports the change;
- preserve unresolved meaning explicitly;
- merge duplicates only when their analytical identity is genuinely the same.

## 7. Lifecycle states

Use at least these states:

### `active`

The finding remains relevant and not fully resolved.

### `resolved`

The finding has an evidence-backed resolution that no longer requires active attention. Preserve the resolution rather than deleting the finding.

### `superseded`

A later finding represents the same analytical concern more accurately. Record `superseded_by` when possible.

### `promoted`

The finding contributed to authoritative semantic knowledge through the normal Semantic Git governance flow. Record resulting semantic references when available.

Promotion does not mean the finding itself became authoritative.

## 8. Semantic status

`semantic_status` must distinguish analytical knowledge from semantic authority.

Useful states include:

```text
unresolved
non_semantic
candidate
promoted
```

Interpretation:

- `unresolved` — behavior/evidence is material but durable semantic meaning is not established;
- `non_semantic` — evidence supports that the finding is physical, historical or otherwise not a domain rule;
- `candidate` — evidence suggests durable semantic meaning, but normal CHANGE/governance is still required;
- `promoted` — the semantic meaning has entered R/D/O through approved governance.

A mathematical contradiction between a governed rule and one consumer is commonly `non_semantic`: the semantic rule may already be settled while the implementation diverges. A genuine missing mathematical convention can remain `unresolved` or become `candidate` if evidence suggests a durable domain rule.

Do not mark a finding `promoted` merely because an AI believes it sounds semantic.

## 9. Risk

Risk explains why the finding deserves retention.

It should answer:

> What material error, divergence or investigation cost could result if this finding were forgotten?

Prefer concrete consequences such as:

- a reimplementation may produce different results for a known boundary case;
- one semantic version may accidentally inherit behavior from another;
- a missing external calendar prevents exact reconstruction;
- an apparently anomalous condition may be removed as a bug without understanding its historical role;
- a consumer may return `NULL` where the governed metric requires zero;
- two aggregation orders may produce different published results;
- an uncovered interval may make a rule partial for admissible inputs.

Risk is analytical context, not proof of semantic meaning.

### Answering questions about domain risk

When the human asks questions such as:

```text
quais riscos conhecidos existem neste domínio?
quais fragilidades conhecidas existem neste namespace?
o que pode dar errado numa reimplementação?
quais exceções ou lacunas merecem atenção?
quais inconsistências matemáticas conhecidas existem?
```

use relevant findings as the evidence-backed map of **known analytical risks** for the namespace. Prefer active or otherwise still-relevant findings, and summarize for each material item:

- finding identity;
- category/status;
- risk level when recorded;
- concrete consequence;
- evidence/certainty when relevant;
- mathematical witness/classification when present;
- whether semantic meaning is unresolved, non-semantic, candidate or promoted.

Do not silently broaden this into a generic enterprise, operational, security or business-risk register unless evidence in scope supports those categories. `_memory` answers what is **known and recorded analytically**, not every risk that could hypothetically exist.

Absence of matching findings means only that no analytical risk was recorded or recovered in the consulted scope. It does not prove that the domain has no risk or no mathematical gap.

## 10. Provenance and evidence

A finding must remain traceable to evidence sufficient to reopen the investigation.

Prefer stable locators when available:

- repository identity;
- commit or tag;
- path;
- symbol, rule or human-readable locator;
- source document;
- evidence boundary or version applicability.

For mathematical findings, also preserve the smallest useful proof artifact: witness input, boundary, interval, algebraic relation, unit mismatch or deterministic check result.

Do not copy large source fragments into memory when a durable locator is sufficient.

The original evidence remains authoritative for what physically existed. `_memory` is an index of material understanding, not a replacement for evidence.

## 11. Reading memory by progressive disclosure

Do not load `_memory` in ordinary namespace bootstrap by default.

Consult it when the task materially benefits from analytical history, including:

- semantic reconstruction;
- reimplementation;
- conceptual review of a reconstruction;
- mathematical review of known quantitative fragilities;
- risk assessment;
- debugging surprising behavior;
- resolving or reopening `REVIEW`;
- asking why a rule or exception exists;
- investigating known edge cases or version boundaries.

Prefer selective retrieval of relevant findings when tooling permits instead of injecting a large memory file into every context.

## 12. Interaction with semantic-extraction

When human-authored sources contain a material observation that should not enter the persistent semantic contract:

1. keep it out of R/D/O;
2. test whether it satisfies the retention test;
3. if yes, use this skill to upsert it into `_memory`;
4. record its human source and uncertainty accurately.

Do not copy whole documents into memory.

## 13. Interaction with semantic-reconstruction

Reconstruction is the primary producer of physical findings.

Before deep investigation, inspect relevant existing memory when it may constrain the target, version or known risks.

During reconstruction, retain findings such as:

- hardcoded exceptions whose behavioral effect is proven but business meaning is unclear;
- physical behavior deliberately excluded from R/D/O by the reimplementation test;
- unresolved evidence gaps that materially affect reconstruction;
- implementation hazards that a future rewrite could accidentally erase.

When reconstruction delegates quantitative analysis to `semantic-mathematical-review`, retain only the resulting mathematical issues that independently pass this skill's retention test.

A finding is not a substitute for continuing the authorized investigation. Do not use memory to justify premature `REVIEW`.

## 14. Interaction with semantic-conceptual-review

Conceptual review may use findings as non-authoritative context, but must reopen original evidence for material conclusions when possible.

It may:

- confirm and enrich a finding;
- merge analytical duplicates;
- reclassify semantic status;
- resolve a finding;
- mark one as superseded;
- identify a finding as a candidate for semantic promotion.

It must not silently delete a material finding merely because that finding was excluded from revised R/D/O.

It should also challenge duplication: if revised R/D/O now adequately owns a semantic proposition, the corresponding active finding must either be resolved/reclassified or, after approved promotion, retained only as `promoted` provenance rather than a parallel semantic statement.

## 15. Interaction with semantic-mathematical-review

`semantic-mathematical-review` discovers whether a quantitative rule is undefined, underdetermined, contradictory, incomplete at boundaries, order-sensitive, precision-sensitive or dimensionally inconsistent. This skill decides only whether that analytical result deserves persistence and how to reconcile it with existing findings.

Typical flow:

```text
semantic-mathematical-review
-> proof / counterexample / witness
-> classify mathematical issue
-> semantic-memory retention test
-> upsert F-* only if material
```

Do not store all mathematical checks. Preserve the issue, not the whole reasoning process.

When authoritative R/D/O already determines the special case, store a material implementation mismatch as a divergence/risk finding rather than pretending the semantic rule is unresolved.

When the mathematical review proves a gap that requires a new business convention, memory may preserve the unresolved gap, but only CHANGE + human approval can define the new semantic rule.

## 16. Promotion to R/D/O

Promotion follows the normal Semantic Git flow:

```text
finding
-> additional evidence / semantic understanding
-> CHANGE or existing authorized CHANGE
-> semantic review
-> human approval
-> R/D/O
```

`semantic-memory` cannot bypass this flow.

After promotion, retain the finding when its provenance remains useful:

```yaml
status: promoted
semantic_status:
  state: promoted
semantic_refs:
  - domain/example:D-007
```

The authoritative current semantic statement now lives in R/D/O. Do not maintain a second normative copy of that rule in `_memory`; retain only the analytical history needed to understand where it came from and point to the semantic authority through `semantic_refs`.

Do not rewrite history to pretend the semantic meaning was always known.

## 17. Publication boundary

`_memory` is excluded from canonical publication by default.

A publication intended to explain analytical history may include selected findings only through an explicit, separate publication mode or human request. Such publication does not make findings authoritative.

## 18. Memory gates

Before writing or updating `FINDINGS.yaml`, verify:

1. **Namespace** — the finding belongs to this namespace.
2. **Materiality** — it is worth retaining.
3. **Evidence** — observation/inference is traceable.
4. **Non-authority** — it is not being used to bypass R/D/O governance.
5. **Deduplication** — an equivalent `F-*` does not already exist under another ID.
6. **Identity** — updates preserve stable finding identity.
7. **Required fields** — all minimum fields exist.
8. **Lifecycle** — status reflects current analytical state.
9. **Risk** — the retention consequence is explicit.
10. **No silent loss** — existing unexamined findings remain intact.
11. **Progressive disclosure** — memory is not added to default context or publication without reason.
12. **Draft boundary** — when the related CHANGE is `DRAFT`, the write is analytical memory only, derives from the authorized investigation, and does not edit or materialize R/D/O or implementation.
13. **R/D/O exclusivity** — an active finding does not duplicate a proposition already adequately owned by authoritative R/D/O; promoted findings point to semantic authority instead of becoming a second source of truth.
14. **Risk-query discipline** — risk summaries report evidence-backed analytical risks actually present in relevant findings and do not infer absence of risk from absence of findings.
15. **Mathematical discipline** — mathematical findings preserve the issue, proof/witness and risk without turning engine behavior into semantic authority or creating a parallel mathematical specification.

If a required fact is unknown, represent it as unknown or unresolved instead of inventing it.

## Final rule

Preserve what would be expensive or dangerous to forget, but do not confuse remembering with governing.

```text
observe
-> decide whether forgetting is materially risky
-> preserve the finding with evidence and risk
-> reconcile it over time
-> promote only through normal semantic governance
```
