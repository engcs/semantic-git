---
name: semantic-extraction
description: Use when extracting human-readable semantic essence from code, SQL, dbt models, data pipelines, documents, or existing systems into Semantic Git CHANGE or R/D/O artifacts. Separates evidence from durable meaning, subtracts inherited knowledge, and prevents implementation detail from overwhelming the contract.
compatibility: Semantic Git 1.5
---

# Semantic Extraction

Produce the smallest faithful semantic contract that lets a human understand the subject and lets a future implementation preserve its meaning.

This skill derives its authority from `SEMANTIC_GIT.md`. It summarizes a method; it does not create normative rules. Consult the specification progressively, especially sections 8-9, 13.8, 23.3, 24.4 and 26, plus applicable domain foundations.

## Core distinction

Keep three products separate:

1. **Evidence map** - where each interpretation came from, with paths, lines, confidence and conflicts.
2. **Semantic model** - the internal classification of purpose, facts, population, rules, boundaries and inheritance.
3. **Persistent contract** - only the durable Requirements, Decisions and Operations that belong to the target namespace.

Evidence supports the contract. It does not automatically belong inside it.

## Workflow

### 1. Establish authority and scope

- Identify the target Semantic Namespace and applicable ancestors.
- Read their Requirements, then Decisions, then Operations.
- Read only enough physical material to understand the subject and trace necessary dependencies.
- For any governed writing, follow the complete Execution Protocol in section 24.4 and the authorization gates in section 13.8 before writing.

### 2. Build an evidence map

For every relevant finding, record its source and classify it as:

- inherited from an ancestor;
- common knowledge that belongs in an ancestor;
- specific to the target;
- specific to another consumer or version;
- physical implementation only;
- ambiguous and requiring `REVIEW`.

Do not write the persistent contract during this pass.

### 3. Form the semantic core

Explain the subject without implementation vocabulary:

- purpose: what problem or question it addresses;
- elementary fact: the occurrence being classified or measured;
- inputs or measures: what contributes to the result;
- population: which occurrences are eligible;
- contribution rules: when an occurrence contributes to each measure;
- time: reference period, validity and relevant temporal boundaries;
- recuts: business views or segments that change participation;
- aggregation: how elementary contributions become published results;
- edge cases: behavior that materially changes interpretation.

If these cannot be stated clearly, continue investigating or produce `REVIEW`.

### 4. Subtract before writing

Remove an item when any test below succeeds:

- **Inheritance test:** it remains true solely because an ancestor already governs it.
- **Rewrite test:** an equivalent reimplementation could replace it without changing meaning.
- **Consumer test:** it belongs to another version, indicator or consumer.
- **Evidence test:** it proves a conclusion but is not itself durable knowledge.
- **Naming test:** it is only a table, column, flag, model, alias or pipeline-stage name without independent semantic evidence.

Do not create one contract item for every topic investigated. Investigation must be broad; persistence must be selective.

### 5. Write R/D/O

- **Requirements:** truths necessary for the purpose to hold.
- **Decisions:** durable choices that define how Requirements are satisfied, including formulas, population boundaries and interpretations.
- **Operations:** only the behavior needed to realize and preserve those Decisions in practice.

Keep causal links visible, such as `Atende R-A`, but do not force one-to-one chains.

Names of models, SQL expressions, paths and fields may appear in Operations only when they are durable operational dependencies. Do not use Operations as an evidence ledger or lineage dump.

For a governed new namespace, use its unique `CHANGE-INIT` and express the proposed R/D/O as concise `ADD` entries in the Semantic Diff. Do not create `CHANGE-INIT` for a namespace with pre-existing AS-IS. Use local aliases until promotion under the repository policy.

## Compression gates

Before presenting the result, apply all gates:

1. **Human reading:** can a domain reader explain the subject after one short reading?
2. **Reimplementation:** would the contract remain valid if the physical solution were rewritten?
3. **Inheritance:** was ancestral meaning referenced rather than copied?
4. **Reconstruction:** can another person implement the essential behavior without inventing business rules?
5. **Evidence:** does every persisted claim have support or explicit human intent?
6. **Economy:** can any item be removed without losing meaning, boundary or reconstructibility?

If an item fails economy, remove or merge it. If it fails evidence or reconstruction, use `REVIEW` rather than adding technical detail to hide the gap.

Also execute the canonical R/D/O gate in section 23.3: every Requirement needs a corresponding Decision; every Decision needs an Operation when materialized; Decisions must remain free of physical details; and Operations must not create new semantic rules.

## Contrast check

Test the draft against both scenarios:

- **Mechanical extraction:** the output mirrors files, columns, lineage, flags and every investigated topic. Reject it even when fully traceable.
- **Semantic extraction:** the output explains purpose, population, contribution rules, boundaries and aggregation, while evidence remains outside the persistent contract. Accept it only when the compression gates also pass.

If removing implementation names makes the draft unintelligible, recover the missing business meaning instead of restoring the implementation inventory.

## Anti-patterns

Reject outputs that:

- copy the evidence map into the CHANGE or R/D/O;
- turn every source column or status into a concept;
- repeat identity, publication, history or expurgo rules already inherited;
- persist lineage, debug fields, joins or intermediate stages by default;
- treat observed code behavior as human intent without evidence;
- maximize coverage at the cost of readability;
- use a passing structural validator as proof of semantic quality.

## Output discipline

Present in this order:

1. evidence map, when requested;
2. classifications and material `REVIEW` items;
3. concise proposed Semantic Diff or R/D/O;
4. gate result and unresolved decisions.

The persistent artifact should contain item 3 and required CHANGE metadata, not the full analysis trail.

Prefer a short contract that preserves purpose and behavior over a comprehensive description of the current implementation.
