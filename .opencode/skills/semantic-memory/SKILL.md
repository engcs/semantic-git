---
name: semantic-memory
description: Use to read, create, reconcile or update a Semantic Namespace analytical memory in _memory/FINDINGS.yaml. Preserves material findings, exceptions, risks, unresolved meaning and evidence that are costly or dangerous to rediscover but are not authoritative R/D/O. This skill is transversal and does not replace Semantic Git governance.
compatibility: Semantic Git 1.5
---

# Semantic Memory

Manage the analytical memory of a Semantic Namespace without turning analysis into semantic authority.

This skill derives all normative authority from `SEMANTIC_GIT.md`. It is a transversal capability used by `semantic-extraction`, `semantic-reconstruction`, `semantic-conceptual-review`, reimplementation, risk analysis and debugging when analytical findings must survive beyond one session.

## Fundamental distinction

```text
R/D/O
= what is semantically authoritative now

_memory/FINDINGS.yaml
= what is important not to forget

Git / source implementation
= original physical evidence
```

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
- physical constraints that are important to preserve but not yet justified as domain rules.

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
- hidden place to persist a semantic rule without governance.

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

Do not fabricate source paths, commits, certainty, rationale or human intent.

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

Do not mark a finding `promoted` merely because an AI believes it sounds semantic.

## 9. Risk

Risk explains why the finding deserves retention.

It should answer:

> What material error, divergence or investigation cost could result if this finding were forgotten?

Prefer concrete consequences such as:

- a reimplementation may produce different results for a known boundary case;
- one semantic version may accidentally inherit behavior from another;
- a missing external calendar prevents exact reconstruction;
- an apparently anomalous condition may be removed as a bug without understanding its historical role.

Risk is analytical context, not proof of semantic meaning.

## 10. Provenance and evidence

A finding must remain traceable to evidence sufficient to reopen the investigation.

Prefer stable locators when available:

- repository identity;
- commit or tag;
- path;
- symbol, rule or human-readable locator;
- source document;
- evidence boundary or version applicability.

Do not copy large source fragments into memory when a durable locator is sufficient.

The original evidence remains authoritative for what physically existed. `_memory` is an index of material understanding, not a replacement for evidence.

## 11. Reading memory by progressive disclosure

Do not load `_memory` in ordinary namespace bootstrap by default.

Consult it when the task materially benefits from analytical history, including:

- semantic reconstruction;
- reimplementation;
- conceptual review of a reconstruction;
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

## 15. Promotion to R/D/O

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

Do not rewrite history to pretend the semantic meaning was always known.

## 16. Publication boundary

`_memory` is excluded from canonical publication by default.

A publication intended to explain analytical history may include selected findings only through an explicit, separate publication mode or human request. Such publication does not make findings authoritative.

## 17. Memory gates

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
