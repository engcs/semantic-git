---
name: semantic-extraction
description: Use when durable domain knowledge is already expressed in human-authored sources such as requirements, policies, decisions, specifications, interviews, diagrams, or documentation and must be compressed into Semantic Git R/D/O or CHANGE artifacts. Do not use as the primary method when the business meaning must be reverse-engineered from implementation behavior; use semantic-reconstruction instead.
compatibility: Semantic Git 1.5
---

# Semantic Extraction

Produce the smallest faithful semantic contract from knowledge that is already substantially expressed in human-readable form.

This skill derives its authority from `SEMANTIC_GIT.md`. It summarizes a method; it does not create normative rules. Consult the specification progressively, especially sections 8-9, 13.8, 23.3, 24.4 and 26, plus applicable domain foundations.

## Role in the semantic skill suite

Use the three semantic skills according to the source of knowledge and the stage of work:

```text
human knowledge already expressed
-> semantic-extraction

business meaning hidden in an existing implementation
-> semantic-reconstruction

candidate R/D/O needs senior conceptual criticism
-> semantic-conceptual-review
```

`semantic-memory` is a transversal capability, not a fourth semantic stage. Use it when extraction discovers a material fact, exception, risk, evidence gap or unresolved meaning that should survive beyond the session but should not become authoritative R/D/O.

Extraction is not reverse engineering. Code snippets or physical artifacts may be used as supporting evidence, but if the essential business meaning must be inferred from behavior distributed through implementation, switch to `semantic-reconstruction`.

## Core distinction

Keep these products separate:

1. **Evidence map** — where each interpretation came from, with source, confidence and conflicts.
2. **Semantic model** — the internal classification of purpose, facts, population, rules, boundaries and inheritance.
3. **Persistent contract** — only the durable Requirements, Decisions and Operations that belong to the target namespace.
4. **Analytical memory, when warranted** — selected material findings that are costly or dangerous to forget but do not belong in the persistent contract.

Evidence supports the contract. It does not automatically belong inside it. Analytical memory preserves selected findings; it does not make them semantic authority.

## 1. Establish authority and scope

- Identify the target Semantic Namespace and applicable ancestors.
- Read their Requirements, then Decisions, then Operations.
- Identify which human-authored sources are authoritative, explanatory or merely contextual.
- Respect any explicit evidence boundary imposed by the human.
- For governed writing, follow the applicable authorization and execution rules in `SEMANTIC_GIT.md`.

Do not persist local knowledge before inheritance is understood.

Do not load `_memory` by default merely because it exists. Consult it when the task concerns prior findings, known risk, unresolved `REVIEW`, reimplementation or another case where analytical history is materially relevant.

## 2. Build an evidence map

For every relevant finding, record its source and classify it as:

- inherited from an ancestor;
- common knowledge that belongs in an ancestor;
- specific to the target;
- specific to another consumer or version;
- physical implementation only;
- ambiguous and requiring `REVIEW`.

Do not write the persistent contract during this pass.

When sources conflict, preserve the conflict explicitly rather than silently choosing the most convenient wording.

When a finding will be excluded from R/D/O but forgetting it would materially increase rediscovery cost or risk, apply `semantic-memory` and reconcile it with the namespace's existing `_memory/FINDINGS.yaml` instead of copying the complete evidence map into memory.

## 3. Form the semantic core

Explain the subject without implementation vocabulary.

Investigate, when applicable:

- purpose: what problem, need or question the subject addresses;
- elementary fact or entity: what is independently meaningful;
- population: which occurrences or entities are in scope;
- inputs, measures or states: what contributes to meaning or outcome;
- contribution or classification rules;
- temporal semantics and validity boundaries;
- business recuts or views;
- aggregation or composition;
- formulas when they are business rules;
- material edge cases.

Do not force every category to exist. The semantic model must follow the sources, not a template.

If a material concept cannot be stated clearly from the available human knowledge, continue investigating the authorized sources or produce `REVIEW`.

## 4. Distinguish stated meaning from implementation observation

Human-authored sources can still contain technical detail.

For each finding ask:

- Is this a durable domain rule or only the current way of implementing it?
- Would this statement remain true after a full technology rewrite?
- Is this explaining intent, meaning or merely mechanism?

Do not elevate observed physical behavior to human intent unless the sources support that interpretation.

If the task requires deriving missing meaning from physical behavior, hand off that part to `semantic-reconstruction`.

A physical or historical observation that fails the reimplementation test may still qualify for `_memory` when its loss would create material risk. Exclusion from R/D/O does not imply irrelevance.

## 5. Subtract before writing

Remove an item from the persistent contract when any test below succeeds:

- **Inheritance test:** it remains true solely because an ancestor already governs it.
- **Rewrite test:** an equivalent reimplementation could replace it without changing meaning.
- **Consumer test:** it belongs to another version, indicator or consumer.
- **Evidence test:** it proves a conclusion but is not itself durable knowledge.
- **Naming test:** it is only a table, column, flag, model, alias or pipeline-stage name without independent semantic meaning.

After subtraction, evaluate material excluded findings with the `semantic-memory` retention test. Do not use memory to rescue every discarded detail.

Do not create one contract item for every topic investigated. Investigation may be broad; persistence must be selective.

## 6. Write R/D/O

### Requirements

Express durable truths, needs and invariants necessary for the subject's purpose.

### Decisions

Express durable choices that define how Requirements are satisfied, including formulas, population boundaries, semantic interpretations or conventions when supported.

### Operations

Express only the behavior needed to realize and preserve the Decisions in practice.

Keep causal links visible, such as `Atende R-A`, but do not force one-to-one chains.

Names of models, SQL expressions, paths and fields may appear in Operations only when they are themselves durable operational dependencies. Do not use Operations as an evidence ledger or lineage dump.

For a governed new namespace, use its unique `CHANGE-INIT` and local aliases until promotion under repository policy. Do not create `CHANGE-INIT` for a namespace with pre-existing AS-IS.

## 7. Compression gates

Before presenting the result, apply all gates:

1. **Human reading** — can a domain reader explain the subject after one short reading?
2. **Reimplementation** — would the contract remain valid if the physical solution were rewritten?
3. **Inheritance** — was ancestral meaning referenced rather than copied?
4. **Reconstruction** — can another person implement the essential behavior without inventing business rules?
5. **Evidence** — does every persisted claim have support or explicit human intent?
6. **Economy** — can any item be removed without losing meaning, boundary or reconstructibility?
7. **R/D/O separation** — does each artifact have its canonical role under `SEMANTIC_GIT.md`?
8. **Memory retention** — were materially risky or expensive-to-rediscover excluded findings preserved selectively without promoting them to authority?

If an item fails economy, remove or merge it. If it fails evidence or reconstruction, use `REVIEW` rather than adding technical detail to hide the gap. If it is excluded from R/D/O but passes the memory retention test, upsert it through `semantic-memory`.

## 8. Contrast check

Reject both failure modes:

### Mechanical extraction

The output mirrors documents section by section, copies implementation names, or turns every sentence into a contract item.

### Semantic extraction

The output explains purpose, population, rules, boundaries and material behavior while evidence remains outside the persistent contract.

If removing source wording makes the draft unintelligible, recover the missing meaning instead of copying the source structure.

## 9. Anti-patterns

Reject outputs that:

- copy the evidence map into the CHANGE, R/D/O or `_memory`;
- turn every source term into a concept or finding;
- repeat identity, publication, history or expurgo rules already inherited;
- persist lineage, debug fields, joins or intermediate stages by default;
- treat implementation behavior as human intent without evidence;
- use `_memory` as a hidden semantic contract;
- append a duplicate finding on every execution instead of reconciling stable `F-*` identity;
- delete existing memory merely because the current extraction did not encounter it;
- maximize coverage at the cost of readability;
- use a structural validator as proof of semantic quality;
- attempt reverse engineering with this skill when `semantic-reconstruction` is the appropriate method.

## 10. Output discipline

Present in this order:

1. evidence map, when requested;
2. classifications and material `REVIEW` items;
3. concise proposed Semantic Diff or R/D/O;
4. material analytical-memory updates, when any were warranted;
5. gate result and unresolved decisions.

The persistent semantic artifact should contain the proposed contract and required governance metadata, not the full analysis trail. `_memory/FINDINGS.yaml` is a separate non-authoritative artifact governed by `semantic-memory`.

## Handoff to conceptual review

When the extracted contract is materially complex, high-impact, or still reads like the wording of its source rather than a coherent domain model, pass the candidate to `semantic-conceptual-review` together with:

- candidate R/D/O;
- evidence map;
- original relevant sources;
- applicable ancestral R/D/O;
- remaining `REVIEW` items;
- relevant analytical findings from `_memory`, when they materially constrain the review.

The conceptual reviewer must be allowed to preserve the candidate unchanged when it is already adequate. Findings remain non-authoritative context and should be checked against original evidence when they materially affect the review.

## Final rule

Prefer a short contract that preserves purpose and behavior over a comprehensive restatement of the source material, while preserving separately the small set of non-semantic findings that would be costly or dangerous to forget.

```text
understand the human knowledge
-> separate evidence from meaning
-> subtract inheritance
-> retain material non-semantic findings when warranted
-> compress without semantic loss
-> persist durable R/D/O
```
