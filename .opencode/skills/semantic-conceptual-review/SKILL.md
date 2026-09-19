---
name: semantic-conceptual-review
description: Use after a candidate Semantic Git R/D/O has been extracted or reconstructed and needs a senior conceptual review. Reopens evidence when necessary, elevates behavioral descriptions into human domain concepts, removes residual implementation language, challenges premature REVIEW, and preserves evidence, inheritance and reconstructibility. This is not a prose-polishing skill.
compatibility: Semantic Git 1.5
---

# Semantic Conceptual Review

Review a candidate semantic contract as a senior domain modeler: understand what the evidence means as a coherent system of ideas, then revise R/D/O so that it expresses the domain rather than the path used to discover it.

This skill derives normative authority from `SEMANTIC_GIT.md`. It complements `semantic-extraction` and `semantic-reconstruction`; it does not replace either one.

## Role in the semantic skill suite

Use the three skills according to the source of knowledge and the stage of work:

```text
knowledge already explicit in human sources
-> semantic-extraction

knowledge implicit in an existing implementation
-> semantic-reconstruction

candidate R/D/O already exists and needs conceptual criticism
-> semantic-conceptual-review
```

`semantic-memory` is transversal, not a fourth semantic stage. Use it when review changes the analytical status of material findings that should survive beyond the review but should not be treated as authoritative R/D/O.

`semantic-mathematical-review` is also transversal. Use it when a candidate contains material formulas, aggregations, limits or piecewise quantitative rules whose domain, totality, uniqueness, boundaries, aggregation order, precision or dimensional consistency have not been demonstrated. Mathematical review supplies specialized evidence; conceptual review remains responsible for deciding what that evidence means for the semantic contract.

The review stage is especially valuable after reconstruction, because a behaviorally correct first pass may still speak like an engineer reading code rather than a domain expert explaining the business.

## Fundamental objective

The objective is not to make the candidate sound nicer.

The objective is:

> transform a faithful behavioral model into the clearest durable conceptual contract supported by the evidence, without losing rules needed to reproduce the behavior.

The desired transformation is:

```text
physical evidence
-> behavioral model
-> conceptual domain model
-> R/D/O
```

Material findings that should not become R/D/O may remain separately in analytical memory:

```text
physical evidence
-> material non-semantic or unresolved finding
-> _memory/FINDINGS.yaml
```

`semantic-reconstruction` is primarily responsible for the first two transitions. This skill concentrates on the transition from behavioral model to conceptual domain model and on critically reviewing the resulting R/D/O.

## Required inputs

Before reviewing, obtain when available:

- target Semantic Namespace;
- applicable ancestral R/D/O;
- candidate R/D/O or Semantic Diff;
- evidence map or equivalent trace of supporting sources;
- original relevant sources;
- identified semantic-version boundary, when applicable;
- unresolved `REVIEW` items;
- relevant findings from `_memory/FINDINGS.yaml`, when analytical history materially constrains the review;
- mathematical review findings/proofs when quantitative closure is material;
- any explicit evidence boundary imposed by the human.

Do not load `_memory` indiscriminately. Read only relevant findings when they can affect known risks, edge cases, unresolved meaning, prior investigation or reimplementation safety.

Do not review from the candidate prose alone when the original evidence is available. A reviewer that cannot reopen evidence can only judge wording and internal consistency, not semantic completeness.

A finding in `_memory` is not authority. When a material conclusion depends on it, reopen original evidence when possible.

A mathematical classification is also not semantic authority. It proves or challenges mathematical properties; the domain meaning of any resolution still requires semantic evidence or normal governance.

If material original evidence is unavailable, state that limitation and do not pretend to have independently validated completeness.

## Capability advisory

Conceptual review is reasoning-intensive because it requires criticism, abstraction, evidence checking and synthesis at the same time.

A skill cannot assume that it can change the runtime model. Model selection belongs to the host, agent, command or human operating the environment.

When the runtime exposes its capability and a materially stronger reasoning configuration is available, recommend using it for this stage.

When capability is unknown, or the current environment is explicitly optimized for speed or cost, emit this short advisory before the review:

> **Capability advisory:** this conceptual review benefits from a high-capability reasoning model. Continue here if desired, or switch to a stronger reasoning configuration before treating the reviewed R/D/O as final.

Do not name a provider or model family in the persistent skill logic. Do not refuse to proceed solely because model capability is unknown or lower than ideal.

## 1. Preserve authority and provenance

Before changing the candidate:

- read applicable ancestral R/D/O;
- identify which candidate claims are inherited, local, physical evidence or unresolved;
- preserve traceability from every material semantic claim back to evidence or explicit human intent;
- preserve the target semantic-version boundary;
- distinguish relevant `_memory` findings from authoritative semantic claims;
- distinguish mathematical proof or counterexample from the semantic convention that may resolve it.

A conceptual improvement that weakens evidence is a regression.

Do not promote a finding merely because it provides a convenient explanation. Semantic authority still requires evidence, CHANGE governance and human approval.

## 2. Reconstruct the domain narrative before editing R/D/O

Do not start by rewriting Requirements sentence by sentence.

First explain the subject in coherent domain language as if speaking to another experienced specialist who must understand the system without seeing the implementation.

The narrative should answer only questions supported by the domain, such as:

- What is being observed, controlled, classified or measured?
- What business problem or distinction gives the subject a reason to exist?
- What is the elementary occurrence or entity of meaning?
- What makes an occurrence relevant or irrelevant?
- What concepts determine contribution, state or outcome?
- Which concepts depend on which others?
- What temporal or validity boundaries materially change meaning?
- Which views or segments represent genuinely different business populations?
- How do elementary facts become a published or actionable result?
- Which edge cases alter interpretation rather than merely implementation?

Do not force every question to have an answer. The purpose is to form a coherent theory of the domain proved by the evidence, not to fill a template.

A known physical exception from `_memory` may constrain this narrative, but if its business meaning remains unresolved, keep that uncertainty explicit instead of making the exception define the domain theory.

## 3. Look for conceptual compression

Compare the candidate's individual rules against the domain narrative.

Ask whether multiple physical or behavioral findings are manifestations of one larger business concept.

Examples of legitimate conceptual compression include:

- several activity flags becoming one eligibility rule;
- several status tests becoming one business classification;
- multiple pipeline steps becoming one durable operational stage;
- a numerator and denominator mechanism becoming a business notion of adherence when the evidence supports that meaning.

Compression is valid only when it preserves all material behavioral distinctions.

Do not merge rules merely to make the contract shorter.

If compression removes physical detail that is not semantically durable but is materially risky to forget, preserve that detail through `semantic-memory` rather than keeping it in R/D/O.

## 4. Elevate purpose above mechanism

Requirements should express why the subject exists or what must remain true, not merely restate how the implementation computes it.

Challenge any Requirement that mainly describes:

- intermediate measures;
- storage or pipeline behavior;
- implementation vocabulary;
- a sequence of calculations with no business purpose;
- generic inherited behavior already governed above.

Ask:

> What durable business truth makes this mechanism necessary?

If the evidence supports a higher-level formulation, prefer it.

If the evidence does not support purpose beyond mechanism, do not invent one; retain the narrower statement or use `REVIEW`.

An unexplained hardcoded behavior can remain a material finding without being elevated to purpose or Decision.

## 5. Remove residual implementation language

Flag candidate language that would become obsolete after a physical rewrite, including unnecessary references to:

- tables or models;
- field names;
- flags;
- IDs;
- joins;
- CASE branches;
- pipeline stages;
- implementation-specific snapshots or aliases;
- incidental architecture.

Translate deterministic physical behavior into the corresponding domain concept when the evidence supports a unique interpretation.

Do not replace a physical term with a vague business-sounding synonym. The replacement must improve semantic meaning.

When a removed physical detail is materially important for future investigation or safe reimplementation, reconcile it into `_memory` if it passes the retention test. Do not preserve every discarded implementation detail.

## 6. Challenge premature REVIEW

For each `REVIEW`, determine whether it is genuinely unresolved or merely under-investigated.

When evidence is available, reopen the relevant sources and try to resolve:

- aliases;
- status mappings;
- code-to-domain translations;
- distributed conditions;
- version applicability;
- inheritance;
- temporal relationships.

A missing human-friendly label does not automatically prevent recovery of the underlying business behavior.

Keep `REVIEW` only when material ambiguity remains or required evidence is genuinely unavailable.

Do not invent labels, intent or rationale to eliminate a legitimate `REVIEW`.

Existing memory may help locate prior evidence or explain why an ambiguity survived, but it must not convert an unresolved issue into certainty by repetition alone.

When a `REVIEW` is resolved, update any corresponding finding through `semantic-memory` rather than leaving stale analytical state.

A mathematical `REVIEW` should likewise survive only after the relevant quantitative evidence was actually tested. If a deterministic proof, boundary witness or authoritative R/D/O resolves it, do not retain ambiguity merely because the original candidate omitted the case.

## 7. Detect missing knowledge

A reviewer is allowed to conclude that the candidate is incomplete.

Compare the domain narrative, evidence, relevant memory and candidate contract and ask:

- Is a material population boundary missing?
- Is a contribution rule implicit but absent?
- Is a temporal boundary necessary to reproduce behavior but omitted?
- Is an edge case behaviorally distinct but lost?
- Is an aggregation or calculation order material to the result?
- Did inheritance subtraction remove information necessary to understand local participation?
- Did compression remove a non-semantic but materially risky finding without preserving it in memory?
- Does every material formula have an evidence-backed admissible domain?
- Is every admissible boundary case assigned exactly one result?
- Could average-of-ratios versus ratio-of-sums, rounding stage or units materially change the result?

When semantic knowledge is missing, recover it from evidence before adding it to R/D/O.

When the missing item is material analytical context rather than durable semantic truth, use `semantic-memory` instead of expanding the contract.

When quantitative closure cannot be established directly, invoke `semantic-mathematical-review` rather than relying on intuition.

## 8. Recheck inheritance

Conceptual review often reveals duplicated ancestral meaning that survived the first pass.

For every candidate item ask:

- Is this actually local?
- Is this only an instance of an inherited rule?
- Does the local contract need only to state where an inherited mechanism participates?

Remove duplicated identity, history, publication, aggregation or audit semantics when already governed by an ancestor, unless a local application point is required for reconstructibility.

Do not move inherited semantic meaning into `_memory`. Memory is not a substitute location for authoritative knowledge.

## 9. Review R/D/O separation

### Requirements

They should express durable domain truths, necessities and purpose.

A strong Requirement often survives radical changes in implementation and remains understandable without knowing how the result is calculated.

### Decisions

They should express durable choices, interpretations, formulas, eligibility criteria, conventions or semantic boundaries that satisfy Requirements.

They must not become an implementation inventory.

A mathematical convention that closes an otherwise undefined business case belongs here only when semantic evidence or approved governance actually establishes it. A database fallback is not enough.

### Operations

They should express the minimum conceptual flow required to materialize the Decisions and preserve behavior.

They may describe ordering when order is semantically material, but should not mirror lineage merely because lineage exists.

### Analytical memory

It should contain only material non-authoritative findings that would be expensive or dangerous to forget. It must not become a fourth R/D/O dimension or a hiding place for semantic rules that have not been governed.

Apply the canonical R/D/O gate in `SEMANTIC_GIT.md` after the conceptual revision.

## 10. Human domain test

After drafting the revised contract, ask:

> Could a competent domain specialist read this once and explain what the subject means, who or what participates, the important rules and how the result behaves, without needing the implementation beside them?

If no, identify whether the failure comes from:

- missing domain concepts;
- overly physical language;
- excessive fragmentation;
- hidden inheritance;
- unexplained relationships;
- genuine lack of evidence.

Fix the semantic cause rather than merely simplifying prose.

The domain reader should not need `_memory` to understand the authoritative contract. Memory exists for analytical depth and risk, not basic semantic comprehensibility.

## 11. Reconstruction and reimplementation tests

The reviewed contract must pass both directions.

### Reconstruction

If the implementation disappeared, could another engineer reproduce materially equivalent business behavior from inherited R/D/O plus the reviewed local contract without inventing rules?

For quantitative behavior, this includes special cases: a future implementer should not need to invent what happens at a zero denominator, uncovered boundary, order-sensitive aggregation or other admissible material edge case.

### Reimplementation

If technology, database, SQL, models, field names and pipeline architecture changed completely, would the reviewed contract remain true?

A conceptual review fails if it becomes more elegant but less reconstructible.

Known non-semantic findings in `_memory` may warn a reimplementation team about unresolved hazards, but they do not compensate for semantic rules missing from R/D/O.

When a mathematical gap exists, separate three outcomes explicitly:

```text
semantic convention already governed -> implementation divergence if physical behavior disagrees
semantic convention genuinely absent -> REVIEW / candidate semantic decision
mathematical issue non-semantic but risky -> analytical memory candidate
```

## 12. Candidate delta

Do not hide how the review changed the contract.

Classify material changes as:

- **KEEP** — already conceptually adequate;
- **REWRITE** — same semantic rule, better domain formulation;
- **MERGE** — multiple candidate items are one durable concept;
- **SPLIT** — one candidate item mixes distinct semantic rules;
- **REMOVE** — inherited, physical, redundant or unsupported;
- **ADD** — material knowledge supported by evidence but missing from the candidate;
- **REOPEN REVIEW** — candidate certainty was not justified;
- **RESOLVE REVIEW** — evidence closes a previous ambiguity.

The delta is analysis evidence; do not persist these labels in final R/D/O unless the governing CHANGE format requires them.

For material items removed because they are physical or unresolved rather than semantic, separately decide whether the corresponding analytical finding should be **KEEP**, **UPSERT**, **RESOLVE**, **SUPERSEDE**, or **PROMOTION CANDIDATE** under `semantic-memory`.

## 13. Reconcile analytical memory

When relevant `_memory` exists or the review discovers a new retention-worthy finding, apply `semantic-memory` after the conceptual decision.

The reviewer may:

- preserve a finding unchanged;
- enrich its evidence;
- merge duplicate findings while preserving stable identity where possible;
- mark a finding `resolved` when evidence closes the analytical issue;
- mark a finding `superseded` when a more accurate finding replaces it;
- mark semantic status as `candidate` when durable domain meaning is now plausible;
- mark `promoted` only after normal Semantic Git governance actually places the meaning in R/D/O.

Do not delete a material finding merely because it disappeared from revised R/D/O.

Do not create a new finding for every conceptual rewrite. The finding must independently pass the retention test.

Mathematical findings follow the same rule: preserve only material gaps/divergences that pass `semantic-memory`; do not store the checklist of successful mathematical checks.

## 14. Guardrails

Do not:

- optimize for prose beauty at the expense of behavior;
- use a benchmark or reference answer as a hidden target during production review;
- introduce business intent not supported by evidence or explicit human input;
- replace precise rules with attractive but vague abstractions;
- collapse materially different behaviors into one concept;
- discard edge cases merely because they are awkward;
- treat confidence from the first agent as evidence;
- treat `_memory` as semantic authority;
- treat a mathematical engine fallback as semantic authority;
- choose an arbitrary convention merely to close an indetermination;
- use a finding to bypass CHANGE and human approval;
- erase a finding because the reviewed contract became cleaner;
- assume that a stronger model is automatically correct.

The reviewer must be able to disagree with the candidate and must also be able to preserve it unchanged when it is already conceptually adequate.

## 15. Canonical review gates

Before presenting the reviewed result, verify:

1. **Authority** — applicable ancestral R/D/O was read.
2. **Evidence preservation** — every material revised claim remains supported.
3. **Conceptual elevation** — the result explains domain meaning rather than discovery mechanics.
4. **Purpose** — purpose is as high-level as evidence permits, but no higher.
5. **Concept coherence** — related rules are grouped without erasing material distinctions.
6. **Physical independence** — incidental implementation vocabulary was removed.
7. **Completeness** — no material behavior proved by evidence is missing.
8. **Inheritance** — ancestral meaning is not duplicated.
9. **REVIEW exhaustion** — unresolved items represent genuine residual ambiguity.
10. **R/D/O separation** — Requirements, Decisions and Operations have distinct roles.
11. **Human domain reading** — a specialist can understand the subject without reading code or `_memory`.
12. **Mathematical closure** — material quantitative rules are total and unique over the supported admissible domain, or the remaining mathematical gap/divergence is explicit and evidence-backed.
13. **Reconstruction** — equivalent behavior can be rebuilt without inventing business rules.
14. **Reimplementation** — the contract survives a physical rewrite.
15. **Economy** — no item can be removed without material semantic loss.
16. **Memory integrity** — material non-semantic findings affected by the review were reconciled without being mistaken for authority or silently lost.
17. **No regression** — conceptual elegance did not reduce fidelity or reconstructibility.

## 16. Output discipline

When performing a conceptual review, present in this order:

1. capability advisory, only when applicable;
2. concise conceptual domain narrative;
3. material review findings;
4. mathematical findings when specialized quantitative review was required;
5. candidate delta;
6. genuine remaining `REVIEW` items;
7. revised local R/D/O or Semantic Diff;
8. analytical-memory changes, when any were warranted;
9. gate results.

Keep implementation evidence outside persistent R/D/O. Keep retained non-authoritative findings in `_memory/FINDINGS.yaml` under `semantic-memory` rules.

Do not persist or merge the reviewed contract merely because this skill produced it. Follow the repository's normal governance and human authorization requirements.

## Handoff contract

A normal reconstruction flow is:

```text
semantic-reconstruction
-> evidence map
-> behavioral semantic model
-> optional semantic-mathematical-review when quantitative closure is material
-> candidate R/D/O
-> selected analytical findings
-> semantic-conceptual-review
-> conceptual domain model
-> reviewed R/D/O
-> reconciled analytical memory
-> governance / human approval
```

`semantic-memory` and `semantic-mathematical-review` participate transversally only when their concerns are material; neither is a mandatory sequential stage.

The conceptual reviewer may return to original evidence, but should not restart the entire investigation without a concrete reason discovered during review.

## Final rule

Do not merely make the candidate more readable.

Make it more conceptually true to the domain while remaining equally or more faithful to the evidence, and preserve separately the few material non-semantic findings that would be costly or dangerous to forget.

```text
understand the candidate
-> reopen evidence where necessary
-> form the domain theory
-> challenge the abstractions
-> prove quantitative closure when needed
-> preserve behavior
-> reconcile material analytical memory
-> express the smallest human semantic contract
```