from collections import Counter
from datetime import date
from fractions import Fraction
import itertools
import threading
import time

from gardavu.calendar import generate_slots
from gardavu.domain import Doctor, Plan, Record, Slot, Span
from gardavu.solver import Cancellation, solve
from gardavu.targets import calculate_targets, scaled_targets, statistics
from gardavu.validation import validate


def problem(slots):
    return Plan(min(s.day for s in slots), max(s.day for s in slots), slots)


def test_homogeneous_32_assignments(rules, doctors):
    slots = generate_slots(date(2027, 2, 1), date(2027, 2, 28), rules)
    result = solve(problem(slots), doctors, rules, [])
    assert result.solver_status in ("FEASIBLE", "OPTIMAL"), result.metadata
    counts = Counter(d for ds in result.assignments.values() for d in ds)
    assert Counter(counts.values()) == {1: 28, 2: 2}
    assert validate(result, doctors, rules, []).ok


def test_six_months_30_doctors(rules, doctors):
    rules.max_seconds = 15
    slots = generate_slots(date(2026, 11, 1), date(2027, 4, 30), rules)
    result = solve(problem(slots), doctors, rules, [])
    assert result.solver_status in ("FEASIBLE", "OPTIMAL"), result.metadata
    assert sum(map(len, result.assignments.values())) == sum(s.required for s in slots)
    assert validate(result, doctors, rules, []).ok
    rows = statistics(result, doctors)
    assert max(r['total'] for r in rows) - min(r['total'] for r in rows) <= 1
    assert len(result.metadata['stages']) > 2


def test_participation_absences_and_return(rules):
    ds = [Doctor("A", id="A", suspensions=[Span("2027-02-01", "2027-02-14")]),
          Doctor("B", id="B"), Doctor("C", id="C", participation=[Span("2027-02-15", "2027-02-28")]),
          Doctor("D", id="D", participation=[Span("2027-02-01", "2027-02-14")])]
    slots = generate_slots(date(2027, 2, 1), date(2027, 2, 28), rules)
    targets = calculate_targets(slots, ds)
    assert targets['A', 'TOTAL'] == targets['C', 'TOTAL'] == Fraction(16, 3)
    assert targets['D', 'TOTAL'] == 8
    assert targets['B', 'TOTAL'] == Fraction(40, 3)
    # Suspension neutralisée ; à son retour, A a la même cible que le nouvel arrivant C.
    ds[0].unavailable = [Span("2027-02-20", "2027-02-20")]
    assert calculate_targets(slots, ds)['A', 'TOTAL'] == targets['A', 'TOTAL']
    rules.min_gap = 1
    result = solve(problem(slots), ds, rules, [])
    assert validate(result, ds, rules, []).ok
    assert all("A" not in result.assignments.get(s.id, []) for s in slots if s.day <= "2027-02-14")


def test_weighted_targets_no_punctual_discount(rules):
    ds = [Doctor("A", id="A", coefficient=.5), Doctor("B", id="B")]
    slots = [Slot(str(n), f"2027-02-{n:02}", "SEMAINE", "19:00", "24:00") for n in (1, 8, 15)]
    ds[0].unavailable = [Span("2027-02-01", "2027-02-01")]
    t = calculate_targets(slots, ds)
    assert t['A', 'TOTAL'] == 1 and t['B', 'TOTAL'] == 2
    result = solve(problem(slots), ds, rules, [])
    assert Counter(d for ids in result.assignments.values() for d in ids) == {'A': 1, 'B': 2}


def test_largest_remainders_conserve_sum():
    values = {str(n): Fraction(1, 30) for n in range(30)}
    scaled = scaled_targets(values)
    assert sum(scaled.values()) == 1000
    assert max(scaled.values()) - min(scaled.values()) == 1


def test_history_boundary_before_and_after(rules):
    ds = [Doctor("A", id="A"), Doctor("B", id="B")]
    current = Slot("now", "2027-02-09", "SEMAINE", "19:00", "24:00")
    for when in ("2027-02-04", "2027-02-12"):
        hist = [Record(Slot("old", when, "SEMAINE", None, None), "A")]
        p = solve(problem([current]), ds, rules, hist)
        assert p.assignments['now'] == ['B']
        assert validate(p, ds, rules, hist).ok


def test_christmas_rotation_and_strict_impossibility(rules):
    ds = [Doctor("A", id="A"), Doctor("B", id="B")]
    s = Slot("noel", "2026-12-25", "FERIE_NUIT", "19:00", "24:00", holidays=("NOEL",))
    hist = [Record(Slot("old", "2024-12-25", "FERIE_JOUR", None, None, holidays=("NOEL",)), "A")]
    result = solve(problem([s]), ds, rules, hist)
    assert result.assignments[s.id] == ['B']
    assert result.metadata['stages'][0]['status'] == 'OPTIMAL'
    rules.holiday_mode = 'STRICT'
    hist.append(Record(hist[0].slot, 'B'))
    result = solve(problem([s]), ds, rules, hist)
    assert result.solver_status == 'INFEASIBLE'
    assert 'interdiction stricte' in ' '.join(result.metadata['errors'])


def test_independent_validation_and_locks(rules):
    ds = [Doctor("A", id="A"), Doctor("B", id="B", unavailable=[Span("2027-02-02", "2027-02-02")])]
    ss = [Slot(str(n), f"2027-02-{n:02}", "SEMAINE", "19:00", "24:00") for n in (1, 2)]
    p = problem(ss)
    p.locks = {'1': ['A'], '2': ['A']}
    result = solve(p, ds, rules, [])
    assert result.solver_status == 'INFEASIBLE'
    p.assignments = {'1': ['B'], '2': ['B']}
    report = validate(p, ds, rules, [])
    assert not report.ok and any('indisponible' in e for e in report.errors)
    assert any('Verrouillage' in e for e in report.errors)


def test_exact_staffing_overlap_and_no_double_slot(rules):
    ds = [Doctor("A", id="A")]
    s = Slot("s", "2027-02-01", "SEMAINE", "19:00", "24:00", required=2)
    p = problem([s]); p.assignments = {'s': ['A', 'A']}
    report = validate(p, ds, rules, [])
    assert any('plusieurs postes' in e for e in report.errors)
    assert solve(problem([s]), ds, rules, []).solver_status == 'INFEASIBLE'


def test_cancel_and_unknown(rules, doctors):
    p = problem(generate_slots(date(2027, 2, 1), date(2027, 2, 28), rules))
    cancel = Cancellation(); cancel.cancel()
    result = solve(p, doctors, rules, [], cancel)
    assert result.solver_status == 'UNKNOWN' and not result.assignments
    rules.max_seconds = .01
    result = solve(p, doctors, rules, [])
    assert result.solver_status == 'UNKNOWN', result.metadata


def test_small_optimum_by_enumeration(rules):
    rules.min_gap = 0
    ds = [Doctor('A', id='A'), Doctor('B', id='B'), Doctor('C', id='C')]
    slots = [Slot(str(n), f'2027-02-{n:02}', 'SEMAINE', '19:00', '24:00') for n in (1, 8, 15, 22)]
    p = problem(slots)
    t = calculate_targets(slots, ds)
    target = scaled_targets({d.id: t[d.id, 'TOTAL'] for d in ds}, salt=f'{p.start}:{p.end}:TOTAL')
    optimum = min(sum(abs(1000 * assignment.count(d.id) - target[d.id]) for d in ds)
                  for assignment in itertools.product([d.id for d in ds], repeat=4))
    result = solve(p, ds, rules, [])
    actual = [d for ids in result.assignments.values() for d in ids]
    assert sum(abs(1000 * actual.count(d.id) - target[d.id]) for d in ds) == optimum
    stages = {s['objective']: s for s in result.metadata['stages']}
    assert stages['Charge globale']['value'] == optimum
    assert stages['Charge globale']['status'] == 'OPTIMAL'


def test_weekday_threshold_and_categories(rules, doctors):
    rules.max_seconds = 12
    ss = generate_slots(date(2027, 2, 1), date(2027, 3, 31), rules)
    result = solve(problem(ss), doctors, rules, [])
    rows = statistics(result, doctors)
    assert validate(result, doctors, rules, []).ok
    assert result.metadata['weekday_threshold'] == 1
    # Les catégories font partie d'une étape distincte prouvée ou explicitement réalisable.
    assert any(s['objective'] == 'Catégories' for s in result.metadata['stages'])
    assert all(sum(r['categories'].values()) == r['total'] for r in rows)


def test_repair_respects_locks(rules):
    ds = [Doctor('A', id='A'), Doctor('B', id='B')]
    ss = [Slot(str(n), f'2027-02-{n:02}', 'SEMAINE', '19:00', '24:00') for n in (1, 8)]
    p = problem(ss); p.assignments = {'1': ['A'], '8': ['B']}; p.locks = {'1': ['A']}
    result = solve(p, ds, rules, [], minimize_changes=True)
    assert result.assignments == p.assignments
    assert validate(result, ds, rules, []).ok
