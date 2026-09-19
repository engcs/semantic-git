---
name: semantic-reconstruction
description: Use when durable business meaning must be reverse-engineered from an existing or legacy implementation. Reconstructs behavior through behavioral closure, separates semantic versions from Git chronology, translates deterministic physical behavior into domain meaning, subtracts inheritance, and produces evidence-backed candidate R/D/O for later conceptual review when needed.
compatibility: Semantic Git 1.5
---

# Semantic Reconstruction

Reconstruct the smallest complete semantic contract capable of reproducing the business behavior of an existing implementation without depending on its current physical form.

This skill derives all normative authority from `SEMANTIC_GIT.md`. It does not create a second specification. Consult that specification progressively, especially sections 8-9, 13.8, 23.3, 24.4 and 26, plus applicable domain foundations.

## Role in the semantic skill suite

Use the three semantic skills according to the source of knowledge and stage of work:

```text
human knowledge already expressed
-> semantic-extraction

business meaning hidden in implementation
-> semantic-reconstruction

candidate R/D/O needs senior conceptual criticism
-> semantic-conceptual-review
```

`semantic-memory` is a transversal capability rather than a fourth semantic stage. Reconstruction is its primary producer of physical findings: use it when the investigation proves a material exception, risk, evidence gap or unresolved behavior that should survive beyond the session but should not become authoritative R/D/O.

`semantic-mathematical-review` is another transversal capability. Delegate to it when reconstructed behavior depends materially on formulas, aggregations, limits, piecewise rules or other quantitative logic whose domain, totality, uniqueness, boundaries, aggregation order, precision or dimensional consistency are not already demonstrated.

`semantic-reconstruction` remains responsible for semantic scope, behavioral closure and candidate R/D/O. Mathematical review returns specialized evidence and classifications; it does not take ownership of the domain contract.

`semantic-reconstruction` is responsible for discovering what the implementation proves. It should produce a faithful behavioral semantic model and candidate R/D/O. It is not responsible for making the result look human at the expense of evidence; difficult conceptual elevation belongs in `semantic-conceptual-review`.

## Fundamental objective

The objective is not to describe what the code contains, and it is not to persist only what is literally stated in one file or commit.

The objective is:

> recover the durable business meaning implemented by the system, with enough semantic completeness that an equivalent implementation could be built without rediscovering or inventing business rules.

Central rule:

```text
compress implementation
not behavior
```

Remove SQL, tables, fields, aliases, pipeline stages and incidental architecture while preserving purpose, population, contribution rules, temporal boundaries, recuts, formulas, aggregation behavior and material edge cases.

Compression into R/D/O must not imply forgetting. A material physical fact can fail the reimplementation test and still deserve retention in `_memory` because losing it would make a future investigation or reimplementation materially riskier.

## Capability advisory

Semantic reconstruction can be reasoning-intensive because it may require tracing distributed evidence, resolving dependencies and aliases, isolating semantic versions, synthesizing multiple physical conditions into one business rule, and deciding whether uncertainty is genuine or merely under-investigated.

A skill cannot assume that it can change the runtime model. Model selection belongs to the host, agent, command or human operating the environment.

Do not block execution solely because the current model is optimized for speed or cost. For simple or well-localized implementations, a general capable model may be sufficient.

For materially complex implementations, especially when rules are distributed, version boundaries are subtle, or many `REVIEW` items are emerging, recommend a stronger reasoning configuration before treating the reconstruction as sufficiently exhaustive.

When capability is unknown and the task is materially complex, emit this short advisory before deep reconstruction:

> **Capability advisory:** this reconstruction involves distributed or ambiguous implementation evidence and may benefit materially from a higher-capability reasoning model. Continue here if desired, or switch to a stronger reasoning configuration to reduce missed dependencies, shallow synthesis, and premature `REVIEW`.

Do not name a provider or model family in persistent skill logic. Preserve enough evidence and structure for later `semantic-conceptual-review`, which benefits even more strongly from high-capability reasoning.

## 1. Establish the semantic target

Before reading implementation details:

- identify the target Semantic Namespace;
- read applicable ancestral Requirements, Decisions and Operations;
- identify the semantic subject being reconstructed;
- identify the target semantic version or behavior when versions exist;
- identify any explicit evidence boundary imposed by the human.

Do not persist local knowledge before inheritance is understood.

When the namespace already contains `_memory/FINDINGS.yaml`, consult only relevant findings when they may affect the target version, known edge cases, reimplementation risk, unresolved `REVIEW` or the scope of investigation. Memory is context, not authority: material conclusions must still be checked against original evidence when available.

## 2. Semantic version is not Git chronology

Never assume:

```text
first commit containing the files
=
first semantic version
```

Git chronology is physical evidence. Semantic versions are behavioral identities.

When the implementation distinguishes V1, V2 or equivalent rule sets, identify which behavior belongs to the requested semantic version independently of when files or commits appeared.

A later physical artifact may still materialize an earlier semantic version.

Therefore:

```text
later commit != later semantic rule
```

and:

```text
one semantic version may span multiple files, layers and physical revisions
```

When the task prohibits use of later versions, interpret "later version" semantically unless the human explicitly restricts Git chronology.

Do not borrow rules that belong exclusively to another semantic version.

Existing memory about another version may guide investigation but must not contaminate the reconstructed contract.

## 3. Build the behavioral closure

Do not stop at the target file, folder, model or commit.

Follow every relevant dependency needed to reconstruct the behavior of the target semantic version, including when necessary:

- upstream transformations;
- downstream calculations;
- shared models;
- macros;
- lookups;
- status mappings;
- calendar logic;
- eligibility calculations;
- aggregation layers;
- formulas;
- shared version-neutral components.

This complete dependency set is the **behavioral closure** of the target.

Physical boundaries do not define semantic boundaries.

Investigation is complete only when the semantic core can be stated without implementation vocabulary or when evidence needed for one of its material parts is genuinely unavailable.

A prior finding in `_memory` never proves behavioral closure. Treat it as a pointer to evidence or a known risk that may need revalidation.

## 4. Keep five products separate

### Evidence map

Record:

- physical source;
- relevant fragment;
- semantic interpretation;
- semantic-version applicability;
- confidence;
- conflicts;
- inheritance classification.

### Behavioral semantic model

Internally reconstruct:

- purpose;
- elementary fact;
- population;
- measures or inputs;
- contribution rules;
- temporal rules;
- validity boundaries;
- business recuts;
- aggregation;
- formulas;
- material edge cases;
- relationships among these concepts.

This model should explain behavior, not physical lineage.

### Candidate persistent contract

Draft only durable local R/D/O after inheritance subtraction and implementation-detail removal.

### Analytical memory

Preserve only selected findings that pass the `semantic-memory` retention test: material observations, exceptions, risks, evidence gaps or unresolved meanings that are costly or dangerous to rediscover but should not be authoritative R/D/O.

Do not copy the evidence map into `_memory`. Reconcile findings by stable `F-*` identity using upsert rather than blind append or blind replacement.

### Review package

Preserve enough evidence, classifications, relevant memory and unresolved questions for `semantic-conceptual-review` to challenge the candidate without restarting blindly.

Evidence supports the contract. Memory preserves selected analytical understanding. Neither is the contract.

## 5. Deterministic semantic interpretation is allowed

Do not confuse interpretation with invention.

When multiple physical conditions deterministically compose one business rule, synthesize their semantic meaning.

For example, several physical activity flags may jointly support a semantic rule describing an eligible organizational population.

Physical names are evidence. The durable rule is the semantic result.

This synthesis is valid when:

1. the relevant dependencies were inspected;
2. the physical behavior is unambiguous;
3. no competing material semantic interpretation remains plausible;
4. the result does not introduce unsupported motivation, intent or rationale.

Do not keep physical names merely because they were used to derive the rule.

When deterministic behavior is proven but its durable business meaning is not, do not force it into a human-sounding Decision. If forgetting that behavior creates material risk, retain it through `semantic-memory` with explicit unresolved semantic status.

## 6. Reconstruct the semantic core before R/D/O

Do not write R/D/O until the following questions are answered or explicitly left as genuine `REVIEW`.

### Purpose

What business question does the subject answer?

Do not replace the purpose with an intermediate calculation when stronger evidence exists.

### Elementary fact

What occurrence is independently classified or measured?

### Population

Which occurrences are eligible?

Include material eligibility boundaries.

### Measures or states

What contributes independently to the result or meaning?

### Contribution or classification rules

Under which conditions does an eligible occurrence contribute or change state?

### Time

Which date or event situates the occurrence? What competence, validity or timeliness boundaries apply?

### Recuts

Which business views or segments alter participation?

### Aggregation

How do elementary contributions become published or actionable results?

### Formula

When a final metric exists, what mathematical relationship transforms its measures?

### Edge cases

What happens for zero denominators, missing values, cancellations, expurgos or other materially different situations?

Do not force every dimension to exist. If one is necessary to reproduce observed behavior, continue investigating before using `REVIEW`.

Material edge cases that remain physical or semantically unresolved are strong memory candidates when their omission could alter reimplementation behavior.

### Mathematical closure when quantitative behavior is material

Do not treat a formula as reconstructed merely because its ordinary-case expression was found. When the result depends materially on quantitative logic and mathematical closure is not obvious, invoke `semantic-mathematical-review` and verify, as applicable:

- admissible domain;
- division-by-zero and `0/0` behavior;
- totality of piecewise rules;
- overlap and uniqueness;
- exact boundary cases;
- aggregation order;
- rounding/truncation stage;
- unit/dimensional compatibility.

Keep three conclusions separate:

```text
mathematical behavior
physical engine behavior
semantic rule
```

If authoritative R/D/O already resolves a special case and the implementation disagrees, classify the issue as materialization divergence rather than reopening the business rule automatically. If no semantic convention resolves a material indetermination, preserve the gap as `REVIEW` and/or a retention-worthy mathematical finding instead of inventing the missing convention.

## 7. REVIEW is the last semantic resort

Do not use `REVIEW` merely because:

- a rule is distributed across files;
- meaning is encoded by flags;
- IDs require a lookup;
- several transformations must be combined;
- a rule is not documented in prose;
- physical names differ from domain terminology.

Before producing `REVIEW`:

1. follow relevant dependencies;
2. resolve aliases;
3. resolve lookups and status mappings;
4. inspect relevant conditions;
5. combine conditions belonging to the same rule;
6. identify semantic-version applicability;
7. translate physical behavior into domain concepts;
8. test whether more than one materially different semantic interpretation remains.

Use `REVIEW` only when ambiguity remains after this process or required evidence is genuinely unavailable.

```text
unknown because not investigated
!= REVIEW

unknown after relevant evidence is exhausted
= REVIEW
```

A later conceptual reviewer may still reopen a `REVIEW`; the first reconstruction is not authority over its own uncertainty.

`_memory` is not a shortcut for investigation and must not justify premature `REVIEW`. It preserves material unresolved findings after relevant evidence has been exhausted or records a known risk while investigation continues.

A mathematical finding is likewise not a shortcut: use `semantic-mathematical-review` to prove or demonstrate the gap before preserving it as memory.

## 8. Subtract inheritance semantically

After reconstructing the complete behavior, classify each finding as:

- inherited from an ancestor;
- common knowledge that should belong in an ancestor;
- local to the target namespace;
- specific to another consumer;
- specific to another semantic version;
- physical evidence only;
- material non-semantic or unresolved analytical finding;
- `REVIEW`.

Do not persist inherited rules as new local identities.

However, inheritance subtraction must not make the local behavior impossible to reconstruct.

A local Operation may describe where or how an inherited mechanism participates in the local flow when that information is necessary for reconstructibility. This does not redefine the ancestral rule.

Subtraction is semantic, not merely textual.

For findings excluded from R/D/O, apply `semantic-memory` selectively. Exclusion from the semantic contract is not sufficient by itself to justify retention.

## 9. Write Requirements from business truth

Requirements express stable truths, necessities and invariants of the target domain.

Prefer business purpose and material boundaries over intermediate mechanics.

Requirements may capture:

- purpose;
- eligible population;
- semantic meaning of measures or states;
- validity conditions;
- required business recuts;
- material invariants.

Do not create one Requirement per physical field or transformation step.

If the evidence only proves mechanism and not a higher-level purpose, do not invent a human-sounding purpose. Preserve the narrower truth where semantically justified, flag the conceptual limitation for review, and retain a material physical exception in memory when forgetting it would be risky.

## 10. Write Decisions from durable conceptual choices

Decisions explain durable choices satisfying Requirements.

They may contain:

- formulas;
- business interpretations;
- eligibility criteria;
- status semantics;
- validity conventions;
- recut definitions;
- temporal interpretations;
- material edge-case semantics.

They must not contain table names, column names, SQL, dbt model names, aliases or incidental architecture unless such an identity is itself durable domain knowledge.

A business formula belongs in Decisions. Its physical computation belongs in Operations.

A mathematically undefined case that requires a domain convention also belongs in Decisions only after evidence or governed human approval determines that convention. Engine fallback alone is not enough.

A one-off or unexplained hardcoded exception must not become a Decision merely because it affects output. Preserve it as a finding when the semantic evidence is insufficient and the risk of forgetting it is material.

## 11. Write Operations as reconstructible behavioral flow

Operations must make behavior reproducible without becoming an implementation inventory.

Prefer a conceptual sequence such as:

```text
elementary occurrence
-> temporal context
-> organizational or domain context
-> eligibility
-> contribution/classification
-> inherited mechanisms
-> aggregation or composition
-> formula/outcome
-> consolidation/publication when applicable
```

Include a step when removing it would force a future implementer to rediscover a business rule or materially important processing order.

Do not include a step merely because it exists physically. Physical details that must not be forgotten but fail the durable semantic test belong in analytical memory, not Operations.

## 12. Reconstruction test

After drafting R/D/O, ask:

> If the current implementation disappeared and another engineer received only the applicable ancestral R/D/O plus this local contract, could they build a behaviorally equivalent implementation without inventing business rules?

If no, recover the missing business meaning.

Do not solve reconstruction failure by copying implementation detail.

Known non-semantic risks in `_memory` can warn a reimplementer about unresolved divergence, but they do not make an incomplete semantic contract complete.

For quantitative rules, reconstruction fails if a future implementer must invent behavior for an admissible mathematical edge case that materially affects the result.

## 13. Reimplementation test

Ask the opposite question:

> If SQL, dbt, database, physical models, field names and pipeline architecture were completely replaced, would this contract still be true?

If no, the contract is too physical.

A valid reconstruction must be both:

```text
reconstructible enough to preserve behavior
+
abstract enough to survive reimplementation
```

When a material observation fails this test but is dangerous to forget, remove it from R/D/O and consider `_memory` rather than discarding it.

## 14. Economy test

Economy means minimum semantic knowledge without loss of:

- purpose;
- boundary;
- business behavior;
- interpretability;
- reconstructibility.

Remove redundant evidence, duplicated inheritance, physical lineage and incidental implementation choices.

Do not remove a business rule merely to make the contract shorter.

Economy of R/D/O does not require analytical amnesia. After compression, retain only the small set of excluded findings whose rediscovery cost or risk is material.

## 15. Version isolation test

When reconstructing one semantic version:

- include rules belonging to the target version;
- include shared version-neutral behavior needed by it;
- exclude behavior introduced only by later semantic versions;
- do not use later semantic behavior as confirmation that an earlier rule existed;
- do not infer semantic evolution merely from physical chronology.

When multiple versions coexist physically, isolate each rule by semantic applicability.

A material cross-version observation that must not contaminate the target may be retained in memory with explicit version applicability.

## 16. Contrast check

Reject both extremes.

### Mechanical extraction

Tables, fields, flags, joins, models and pipeline stages are treated as the contract.

### Defensive under-extraction

Only prose-literal statements are persisted and distributed but resolvable business behavior is prematurely moved to `REVIEW`.

### Semantic reconstruction

Purpose, population, measures, contribution rules, time, validity, recuts, formula, aggregation and edge cases are reconstructed from evidence and persisted independently of physical form.

### Analytical memory

Material physical or unresolved findings that should not pollute R/D/O are retained selectively with evidence, risk and semantic status rather than being silently discarded.

### Mathematical review

Material quantitative rules are challenged for domain, totality, uniqueness, boundaries, aggregation order, precision and dimensions when those properties are not already proven. Mathematical gaps are kept separate from engine behavior and from semantic decisions.

A reconstruction may still be behaviorally correct but conceptually awkward. That is a valid reason for later `semantic-conceptual-review`, not for hiding evidence or inventing meaning here.

## 17. Canonical gates

Before presenting the result, verify:

1. **Authority** — applicable ancestral R/D/O was actually read.
2. **Behavioral closure** — relevant implementation dependencies were exhausted.
3. **Semantic-version isolation** — no rule exclusive to another semantic version contaminated the target.
4. **Purpose** — the business question is explicit to the level supported by evidence.
5. **Population** — eligibility is reconstructible.
6. **Contribution/classification** — each material measure or state has reconstructible rules.
7. **Temporal semantics** — material dates, validity and timeliness rules are known.
8. **Recuts** — material business views are defined when applicable.
9. **Formula** — final mathematical behavior is preserved when applicable.
10. **Mathematical closure** — material quantitative rules have evidence-backed domain, edge-case and aggregation behavior, or a genuine mathematical `REVIEW`/finding remains explicit.
11. **Aggregation/composition** — elementary behavior to published outcome is reconstructible.
12. **Inheritance** — ancestral definitions were not duplicated.
13. **Reimplementation** — the contract survives physical rewrite.
14. **Reconstruction** — equivalent behavior can be recreated without inventing business rules.
15. **Evidence** — every persisted semantic claim is supported.
16. **Economy** — no persisted item can be removed without meaningful loss.
17. **R/D/O separation** — apply the canonical Semantic Git separation gate.
18. **REVIEW exhaustion** — every `REVIEW` represents genuine residual ambiguity after the investigation performed.
19. **Memory retention** — material excluded findings that are costly or dangerous to rediscover were reconciled through `semantic-memory` without treating memory as authority.

Failure of reconstruction must not be hidden by implementation detail. Failure of evidence must produce `REVIEW`. Exclusion from R/D/O must not silently erase a material known risk.

## 18. Output discipline

When analysis is requested, present:

1. applicable inherited R/D/O;
2. evidence map;
3. behavioral semantic model;
4. classifications;
5. mathematical review findings when quantitative logic required specialized analysis;
6. genuine `REVIEW` items;
7. candidate local R/D/O;
8. CHANGE or CHANGE-INIT Semantic Diff when applicable;
9. material `_memory` finding updates, when warranted;
10. gate results;
11. review package for `semantic-conceptual-review` when the contract is materially complex or intended for durable promotion.

Keep the evidence map outside persistent R/D/O. Keep analytical findings in `_memory/FINDINGS.yaml`, not in the semantic contract.

For a governed new namespace, use aliases such as `R-A`, `D-A` and `O-A` until promotion is authorized under Semantic Git.

Do not create a version namespace merely because the implementation contains semantic versions.

## Handoff to conceptual review

When a candidate contract is complex, high-impact, behaviorally correct but linguistically mechanical, or contains important `REVIEW` items, hand off to `semantic-conceptual-review` with:

- target namespace and semantic-version boundary;
- applicable ancestral R/D/O;
- evidence map;
- behavioral semantic model;
- candidate R/D/O or Semantic Diff;
- unresolved `REVIEW` items;
- mathematical review findings/proofs when quantitative closure was material;
- relevant analytical findings from `_memory`;
- original relevant sources or enough access to reopen them.

Do not provide a hidden benchmark or reference answer as input to production review.

The conceptual reviewer may revise, merge, split, remove or add candidate items only when supported by the evidence. Findings are non-authoritative context and should be reconciled through `semantic-memory` when the review changes their analytical status.

## Final rule

The desired artifact is not a description of the current implementation.

It is the durable semantic specification that the current implementation proves, plus a small non-authoritative memory of material findings that would be costly or dangerous to forget.

```text
understand broadly
-> reconstruct behavior
-> prove material quantitative closure when needed
-> subtract inheritance
-> remove physical detail from R/D/O
-> retain material non-semantic findings when warranted
-> produce a faithful candidate contract
-> hand off for conceptual review when warranted
```