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
- any explicit evidence boundary imposed by the human.

Do not review from the candidate prose alone when the original evidence is available. A reviewer that cannot reopen evidence can only judge wording and internal consistency, not semantic completeness.

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
- preserve the target semantic-version boundary.

A conceptual improvement that weakens evidence is a regression.

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

## 7. Detect missing knowledge

A reviewer is allowed to conclude that the candidate is incomplete.

Compare the domain narrative, evidence and candidate contract and ask:

- Is a material population boundary missing?
- Is a contribution rule implicit but absent?
- Is a temporal boundary necessary to reproduce behavior but omitted?
- Is an edge case behaviorally distinct but lost?
- Is an aggregation or calculation order material to the result?
- Did inheritance subtraction remove information necessary to understand local participation?

When knowledge is missing, recover it from evidence before adding it to R/D/O.

## 8. Recheck inheritance

Conceptual review often reveals duplicated ancestral meaning that survived the first pass.

For every candidate item ask:

- Is this actually local?
- Is this only an instance of an inherited rule?
- Does the local contract need only to state where an inherited mechanism participates?

Remove duplicated identity, history, publication, aggregation or audit semantics when already governed by an ancestor, unless a local application point is required for reconstructibility.

## 9. Review R/D/O separation

### Requirements

They should express durable domain truths, necessities and purpose.

A strong Requirement often survives radical changes in implementation and remains understandable without knowing how the result is calculated.

### Decisions

They should express durable choices, interpretations, formulas, eligibility criteria, conventions or semantic boundaries that satisfy Requirements.

They must not become an implementation inventory.

### Operations

They should express the minimum conceptual flow required to materialize the Decisions and preserve behavior.

They may describe ordering when order is semantically material, but should not mirror lineage merely because lineage exists.

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

## 11. Reconstruction and reimplementation tests

The reviewed contract must pass both directions.

### Reconstruction

If the implementation disappeared, could another engineer reproduce materially equivalent business behavior from inherited R/D/O plus the reviewed local contract without inventing rules?

### Reimplementation

If technology, database, SQL, models, field names and pipeline architecture changed completely, would the reviewed contract remain true?

A conceptual review fails if it becomes more elegant but less reconstructible.

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

## 13. Guardrails

Do not:

- optimize for prose beauty at the expense of behavior;
- use a benchmark or reference answer as a hidden target during production review;
- introduce business intent not supported by evidence or explicit human input;
- replace precise rules with attractive but vague abstractions;
- collapse materially different behaviors into one concept;
- discard edge cases merely because they are awkward;
- treat confidence from the first agent as evidence;
- assume that a stronger model is automatically correct.

The reviewer must be able to disagree with the candidate and must also be able to preserve it unchanged when it is already conceptually adequate.

## 14. Canonical review gates

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
11. **Human domain reading** — a specialist can understand the subject without reading code.
12. **Reconstruction** — equivalent behavior can be rebuilt without inventing business rules.
13. **Reimplementation** — the contract survives a physical rewrite.
14. **Economy** — no item can be removed without material semantic loss.
15. **No regression** — conceptual elegance did not reduce fidelity or reconstructibility.

## 15. Output discipline

When performing a conceptual review, present in this order:

1. capability advisory, only when applicable;
2. concise conceptual domain narrative;
3. material review findings;
4. candidate delta;
5. genuine remaining `REVIEW` items;
6. revised local R/D/O or Semantic Diff;
7. gate results.

Keep implementation evidence outside persistent R/D/O.

Do not persist or merge the reviewed contract merely because this skill produced it. Follow the repository's normal governance and human authorization requirements.

## Handoff contract

A normal reconstruction flow is:

```text
semantic-reconstruction
-> evidence map
-> behavioral semantic model
-> candidate R/D/O
-> semantic-conceptual-review
-> conceptual domain model
-> reviewed R/D/O
-> governance / human approval
```

The conceptual reviewer may return to original evidence, but should not restart the entire investigation without a concrete reason discovered during review.

## Final rule

Do not merely make the candidate more readable.

Make it more conceptually true to the domain while remaining equally or more faithful to the evidence.

```text
understand the candidate
-> reopen evidence where necessary
-> form the domain theory
-> challenge the abstractions
-> preserve behavior
-> express the smallest human semantic contract
```
