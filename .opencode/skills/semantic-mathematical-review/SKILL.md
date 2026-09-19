---
name: semantic-mathematical-review
description: Use to investigate mathematical gaps, indeterminations, contradictions, domain violations, boundary cases, aggregation-order effects, precision ambiguity and dimensional inconsistency in Semantic Git knowledge or its implementation. Produces evidence-backed mathematical findings without inventing missing business conventions, and may hand material non-authoritative findings to semantic-memory.
compatibility: Semantic Git 1.5
---

# Semantic Mathematical Review

Investigate whether quantitative rules are mathematically total, unique, internally consistent and semantically aligned over the admissible domain supported by evidence.

This skill derives normative authority from `SEMANTIC_GIT.md`. It is a transversal analytical capability. It does not create a fourth R/D/O dimension, does not replace `semantic-reconstruction` or `semantic-conceptual-review`, and does not promote mathematical observations into domain truth by itself.

## When to use

Use this skill when the human asks for any of the following, or when another semantic investigation encounters the same need:

- mathematical gaps;
- inconsistencies in formulas or quantitative rules;
- indeterminate cases;
- division-by-zero or `0/0` behavior;
- missing or overlapping branches in piecewise rules;
- ambiguous boundaries;
- aggregation-order effects;
- unexplained rounding or truncation;
- unit or dimension incompatibility;
- multiple possible outputs for the same admissible input;
- mismatch between an authoritative mathematical rule and a physical implementation.

Also invoke it from `semantic-reconstruction` or `semantic-conceptual-review` when a material formula, aggregation, limit, function or case distinction appears complete but its totality or uniqueness has not actually been demonstrated.

Do not invoke it merely because a domain contains numbers. Use it when quantitative behavior is material to meaning, reconstruction, risk or correctness.

## Core distinction

Keep three layers separate:

```text
mathematical behavior
= what follows from the expression and its domain

physical behavior
= what a language, database, engine or implementation actually does

semantic behavior
= what the governed domain rule says should happen
```

These layers may coincide, but they are not interchangeable.

Examples:

```text
0 / 0
```

is mathematically undefined in ordinary arithmetic. A database may return `NULL`, raise an error or apply another engine-specific behavior. The domain may independently define the business result as zero. None of those physical outcomes automatically creates semantic authority.

## Fundamental objective

For each material quantitative rule, determine whether every admissible input has exactly one semantically meaningful result supported by the evidence.

The minimum flow is:

```text
rule
-> admissible domain
-> boundary and special cases
-> proof / counterexample / witness
-> observable consequence
-> analytical classification
-> compare with semantic authority and implementation
-> decide REVIEW / materialization divergence / memory / no finding
```

Do not choose a missing business convention merely to make the function total.

## 1. Establish authority and evidence

Before mathematical analysis, identify when available:

- target Semantic Namespace;
- applicable R/D/O;
- formula, quantitative rule or aggregation being analyzed;
- physical implementation or source evidence;
- admissible input domain supported by evidence;
- units or dimensions;
- grain and aggregation hierarchy;
- semantic version or applicability boundary;
- relevant `_memory/FINDINGS.yaml` entries when known mathematical risks may already exist.

Do not infer an input domain from mathematical convenience. If evidence only proves a partial domain, analyze that domain and express conclusions conditionally outside it.

## 2. Normalize the quantitative rule

Rewrite the rule into a form that makes mathematical behavior explicit without changing meaning.

Capture, when applicable:

- variables and constants;
- input domains;
- output domain;
- units;
- piecewise branches;
- inequalities and boundary operators;
- null/missing-value conventions if semantically defined;
- aggregation grain;
- calculation order;
- rounding or truncation stage;
- accumulation or window boundaries.

Normalization is analytical. Do not persist a new formula into R/D/O unless it already follows from semantic authority or enters normal CHANGE governance.

## 3. Test domain validity and totality

Ask whether the expression is defined for every admissible input.

Check as applicable:

- zero denominators;
- `0/0`;
- square roots of negative values in real-valued rules;
- logarithms outside their domain;
- inverse functions outside valid ranges;
- overflow or bounded numeric ranges when material;
- missing values where the semantic rule does not define handling;
- piecewise rules with uncovered regions;
- dates, counts, rates or percentages outside proven admissible boundaries.

Classification candidates include:

```text
undefined_domain
boundary_gap
underdetermined
```

If the problematic input is not proven admissible, report the result conditionally:

> If `x = 0` is admissible, the rule is undefined at that point.

Do not invent `x > 0` merely to eliminate the issue.

## 4. Test uniqueness and overlap

For the same admissible input, ask whether more than one rule or branch can produce materially different outputs.

Look for:

- overlapping piecewise intervals;
- two conditions simultaneously true with different results;
- competing formulas for the same semantic quantity;
- conflicting inherited and local conventions;
- duplicate calculation paths that disagree.

Useful classifications:

```text
overlap
contradiction
underdetermined
```

If overlap exists but all applicable branches produce the same result, record it only when the redundancy itself is materially risky. Mathematical overlap without behavioral ambiguity is not automatically a finding.

## 5. Test boundaries explicitly

Boundary errors are frequently hidden by apparently correct general formulas.

Test, when relevant:

- exact lower and upper bounds;
- just below and just above each threshold;
- equality cases;
- first and last time bucket;
- transition between semantic versions;
- zero and sign changes;
- minimum and maximum representable or allowed values;
- empty sets and singleton sets.

Prefer a small concrete witness when one proves the issue clearly.

Example:

```text
rule A: x < 10
rule B: x > 10
```

Witness:

```text
x = 10
```

Classification:

```text
boundary_gap
```

## 6. Test aggregation semantics

Aggregation often produces mathematically valid but semantically different results.

Explicitly distinguish operations such as:

```text
mean(a_i / b_i)
```

from:

```text
sum(a_i) / sum(b_i)
```

They are generally not equivalent.

Check:

- whether aggregation occurs before or after division;
- weighted versus unweighted averages;
- sum of percentages versus percentage of sums;
- cumulative numerator/denominator versus cumulative published ratios;
- duplicate counting after joins;
- grain changes;
- whether order is mathematically associative or commutative for the operation used.

Use classification:

```text
aggregation_order
```

when different plausible orders produce materially different results and the semantic order is absent, ambiguous or contradicted by implementation.

## 7. Test precision, rounding and truncation

Determine whether precision behavior can alter a material result.

Check:

- rounding before versus after aggregation;
- repeated rounding across stages;
- truncation versus nearest rounding;
- number of decimal places;
- percentage display precision versus stored precision;
- comparisons performed on rounded versus raw values.

Use classification:

```text
precision_unspecified
```

when more than one plausible precision convention changes a material outcome and no semantic convention resolves it.

A display-only difference with no material semantic consequence normally does not justify a finding.

## 8. Test dimensional consistency

When quantities carry units or dimensions, verify that operations are meaningful.

Examples:

- adding hours to counts is invalid without a conversion rule;
- comparing currency with percentage is invalid;
- dividing energy by time produces a rate, not energy;
- aggregating values from incompatible unit systems requires explicit conversion.

Use classification:

```text
dimensional_inconsistency
```

when a material rule combines incompatible quantities without a supported transformation.

Do not invent conversion factors.

## 9. Separate mathematical gaps from materialization divergence

After finding a mathematical problem, compare it with authoritative R/D/O when available.

### Semantic rule already resolves the case

If R/D/O uniquely defines the result, then a physical implementation that behaves differently is a **materialization divergence**, not an unresolved business convention.

Example:

```text
semantic rule:
Programmed = 0 -> KPI = 0

observed consumer:
Executed = 0
Programmed = 0
KPI = NULL
```

The mathematical expression `0/0` is ordinarily undefined, but the semantic domain already closes the case as zero. The finding is therefore a contradiction between materialization and governed behavior.

### Semantic rule does not resolve the case

If multiple conventions remain plausible, do not choose one automatically. Produce `REVIEW` when the unresolved choice belongs to the semantic contract, and consider analytical memory when the gap is material and expensive or dangerous to rediscover.

## 10. Analytical classifications

Use the smallest classification that explains the issue. Canonical analytical families for this skill include:

```text
undefined_domain
underdetermined
contradiction
boundary_gap
overlap
aggregation_order
precision_unspecified
dimensional_inconsistency
```

These labels are analytical. They do not create R/D/O identities or a new normative taxonomy.

When persisting through `semantic-memory`, the generic finding `category` should make the mathematical nature obvious, for example:

```text
mathematical_indeterminacy
mathematical_contradiction
mathematical_boundary_gap
mathematical_overlap
mathematical_aggregation_order
mathematical_precision
mathematical_dimension
```

The more specific skill classification can remain inside an optional `mathematics:` block.

## 11. Evidence standard

A material mathematical finding should contain, when applicable:

- affected expression or rule;
- admissible-domain condition;
- activating condition;
- proof, counterexample or concrete witness;
- expected semantic result when authoritative;
- observed physical result when relevant;
- classification;
- material consequence;
- evidence locator.

Prefer mechanically checkable evidence when possible.

A counterexample is especially valuable because one valid witness is sufficient to disprove claims of totality, uniqueness or equivalence.

## 12. Deterministic and symbolic checks first

Prefer deterministic or symbolic verification when feasible.

Examples include:

- direct arithmetic evaluation;
- interval coverage and overlap checks;
- algebraic comparison;
- unit checking;
- finite boundary enumeration;
- exact evaluation of competing aggregation orders on a witness dataset;
- database tests that assert a governed edge case;
- property-based or symbolic tools when available and justified.

Use AI judgment for tasks such as:

- determining the evidence-backed admissible domain;
- deciding whether a mathematical difference is semantically material;
- interpreting whether two formulas represent the same domain concept;
- deciding whether unresolved behavior requires `REVIEW`;
- deciding whether a finding meets `semantic-memory` retention criteria.

Do not replace an easy deterministic proof with intuition.

## 13. Interaction with semantic-memory

`semantic-mathematical-review` discovers and classifies mathematical issues. `semantic-memory` preserves selected material issues that should survive beyond the investigation.

```text
semantic-mathematical-review
-> discovers/proves a mathematical issue
-> semantic-memory retention test
-> optional _memory/FINDINGS.yaml finding
```

Do not create `_memory` merely because this skill ran. Passed checks, trivial cases and disposable intermediate calculations do not belong in memory.

A mathematical finding remains a normal `F-*` finding. Do not create a separate `MATHEMATICS.yaml` merely to store mathematical findings.

When extra structure improves machine readability, use an optional `mathematics:` block inside the finding. Example:

```yaml
- id: F-004
  status: active
  category: mathematical_contradiction
  summary: >
    A consumer produces NULL for the zero-denominator case although the governed KPI defines zero.
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
  evidence:
    certainty: proven
    sources:
      - locator: governed KPI rule and observed consumer output
  risk:
    level: high
    consequence: >
      Consumers that recalculate the ratio may diverge from the governed result.
  semantic_status:
    state: non_semantic
```

The `mathematics:` block is analytical structure, not a second source of truth. If the rule itself is already in R/D/O, do not duplicate that rule as an active semantic proposition in memory; preserve only the finding, divergence, evidence and risk needed for analytical provenance.

## 14. Interaction with semantic-reconstruction

During reconstruction, delegate to this skill when quantitative behavior materially depends on formulas, aggregations, limits, piecewise rules or edge cases whose mathematical closure is not obvious.

The reconstruction remains responsible for semantic scope, evidence closure and R/D/O. This skill returns mathematical evidence and classifications.

Do not let an engine-specific fallback silently become the reconstructed business rule.

## 15. Interaction with semantic-conceptual-review

During conceptual review, use this skill to challenge apparently complete quantitative Decisions and Operations.

Ask:

- Is the formula total over the admissible domain?
- Is the result unique?
- Are all boundaries defined?
- Is aggregation order semantically fixed where it matters?
- Are precision and units sufficient to reproduce behavior?
- Does the candidate accidentally encode a physical fallback as domain meaning?

A mathematical gap is evidence of incompleteness or divergence. It is not permission to invent the missing rule.

## 16. Canonical validation examples

These examples are deliberately small. They are validation fixtures for reasoning, not domain rules.

### A. Denominator zero / `0/0`

Rule:

```text
KPI = 100 * executed / programmed
```

Input:

```text
executed = 0
programmed = 0
```

Expected analytical result when no special semantic convention exists:

```text
undefined_domain
```

If authoritative R/D/O says `programmed = 0 -> KPI = 0`, then a physical `NULL` result becomes:

```text
contradiction / materialization divergence
```

### B. Piecewise gap

```text
x < 10 -> A
x > 10 -> B
```

Witness:

```text
x = 10
```

Expected:

```text
boundary_gap
```

### C. Overlapping rules

```text
x <= 10 -> 1
x >= 10 -> 2
```

Witness:

```text
x = 10
```

Expected:

```text
overlap + contradiction
```

because both branches apply and disagree.

### D. Average of ratios versus ratio of sums

Data:

```text
(1, 1)
(1, 9)
```

Then:

```text
mean(1/1, 1/9) = 5/9
sum(1,1) / sum(1,9) = 1/5
```

Expected when both orders are plausible and no semantic order is fixed:

```text
aggregation_order
```

### E. Rounding stage

Values:

```text
0.444 + 0.444
```

Rounding each value to one decimal before summing gives `0.8`; summing first and then rounding gives `0.9`.

Expected when the rounding stage is material and unspecified:

```text
precision_unspecified
```

### F. Dimensional incompatibility

Rule:

```text
result = 10 hours + 3 occurrences
```

Expected without an explicit conversion or semantic mapping:

```text
dimensional_inconsistency
```

## 17. Review gates

Before reporting completion, verify:

1. **Authority** — applicable R/D/O was distinguished from implementation evidence.
2. **Domain** — admissible inputs are evidence-backed or limitations are explicit.
3. **Totality** — material inputs were checked for undefined regions.
4. **Uniqueness** — overlapping or competing rules were checked.
5. **Boundaries** — material thresholds and zero cases were tested.
6. **Aggregation** — order-sensitive operations were inspected when applicable.
7. **Precision** — rounding/truncation ambiguity was inspected when material.
8. **Dimensions** — units are compatible or an explicit transformation exists.
9. **Physical separation** — engine behavior was not promoted to semantic truth automatically.
10. **Evidence** — each material issue has a proof, counterexample, witness or equivalent trace.
11. **No invented resolution** — missing conventions remain unresolved when evidence does not decide them.
12. **Memory discipline** — only retention-worthy findings are handed to `semantic-memory`.
13. **R/D/O exclusivity** — memory does not duplicate an already governed semantic rule.

## 18. Output discipline

When performing a mathematical review, present in this order when applicable:

1. scope and authoritative rule;
2. admissible domain and assumptions supported by evidence;
3. checks performed;
4. material findings with classification;
5. proof, witness or counterexample;
6. semantic-versus-physical comparison;
7. consequence/risk;
8. whether the issue is `REVIEW`, materialization divergence, memory candidate or already resolved;
9. passed material gates;
10. limitations.

Do not persist R/D/O, `_memory`, implementation changes or fixes merely because the review identified a problem. Follow the governing Semantic Git authorization for the specific write.

## Final rule

A quantitative rule is not complete merely because it works for ordinary inputs.

```text
prove the domain
-> test the edges
-> seek one result for every admissible input
-> separate mathematics from engine behavior
-> preserve material unresolved risk
-> govern any semantic resolution normally
```
