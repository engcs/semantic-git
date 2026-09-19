#!/usr/bin/env python3
"""Deterministic self-checks for semantic-mathematical-review examples.

These fixtures validate the small canonical examples documented by the skill.
They are not a general symbolic-math engine and do not decide domain semantics.
"""

from __future__ import annotations

from fractions import Fraction


def check_zero_denominator() -> None:
    executed = 0
    programmed = 0
    assert programmed == 0
    # Ordinary arithmetic does not define 0/0. If the semantic contract defines
    # KPI=0, a physical NULL is a materialization contradiction instead.
    semantic_expected = 0
    observed = None
    assert executed == 0 and programmed == 0
    assert semantic_expected == 0
    assert observed is None


def check_piecewise_gap() -> None:
    x = 10
    left = x < 10
    right = x > 10
    assert not left and not right


def check_overlap() -> None:
    x = 10
    branch_a = 1 if x <= 10 else None
    branch_b = 2 if x >= 10 else None
    assert branch_a is not None and branch_b is not None
    assert branch_a != branch_b


def check_aggregation_order() -> None:
    rows = [(1, 1), (1, 9)]
    mean_of_ratios = sum(Fraction(a, b) for a, b in rows) / len(rows)
    ratio_of_sums = Fraction(sum(a for a, _ in rows), sum(b for _, b in rows))
    assert mean_of_ratios == Fraction(5, 9)
    assert ratio_of_sums == Fraction(1, 5)
    assert mean_of_ratios != ratio_of_sums


def check_rounding_stage() -> None:
    values = [0.444, 0.444]
    round_then_sum = sum(round(value, 1) for value in values)
    sum_then_round = round(sum(values), 1)
    assert round_then_sum == 0.8
    assert sum_then_round == 0.9
    assert round_then_sum != sum_then_round


def check_dimensional_incompatibility() -> None:
    left_unit = "hours"
    right_unit = "occurrences"
    assert left_unit != right_unit


def main() -> int:
    checks = [
        check_zero_denominator,
        check_piecewise_gap,
        check_overlap,
        check_aggregation_order,
        check_rounding_stage,
        check_dimensional_incompatibility,
    ]
    for check in checks:
        check()
    print(f"PASS: {len(checks)} mathematical review fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
