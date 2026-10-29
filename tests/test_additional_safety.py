from datetime import date
import itertools

from gardavu.domain import Doctor, Plan, Record, Slot, Span
from gardavu.imports import prepare_history
from gardavu.solver import Cancellation, solve
from gardavu.targets import statistics
from gardavu.storage import Project
from gardavu.validation import validate


def test_no_empty_validation(rules, doctors):
    report = validate(Plan('2027-01-01', '2027-01-01', []), doctors, rules, [])
    assert not report.ok


def test_french_holiday_name_normalized(rules, doctors):
    preview = prepare_history([['d', 'm', 'c', 'f'], ['25/12/2024', 'DEMO-001', 'FERIE_JOUR', 'Noël']],
                              {'date': 'd', 'medecin': 'm', 'categorie': 'c', 'fete': 'f'}, doctors, rules)
    assert preview.records[0].slot.holidays == ('NOEL',)


def test_oldest_known_holiday_preferred(rules):
    doctors = [Doctor('A', id='A'), Doctor('B', id='B')]
    s = Slot('s', '2026-12-25', 'FERIE_JOUR', '08:00', '19:00', holidays=('NOEL',))
    history = [Record(Slot('a', '2024-12-25', 'FERIE_JOUR', None, None, holidays=('NOEL',)), 'A'),
               Record(Slot('b', '2018-12-25', 'FERIE_NUIT', None, None, holidays=('NOEL',)), 'B')]
    result = solve(Plan(s.day, s.day, [s]), doctors, rules, history)
    assert result.assignments['s'] == ['B']
    assert validate(result, doctors, rules, history).repeats


def test_cancellation_keeps_verified_solution(rules):
    doctors = [Doctor('A', id='A'), Doctor('B', id='B')]
    slots = [Slot('1', '2027-02-01', 'SEMAINE', '19:00', '24:00'),
             Slot('2', '2027-02-08', 'SEMAINE', '19:00', '24:00')]
    cancel = Cancellation()
    def progress(label):
        if label == 'Catégories':
            cancel.cancel()
    result = solve(Plan(slots[0].day, slots[-1].day, slots), doctors, rules, [], cancel, progress=progress)
    assert result.assignments and result.solver_status == 'FEASIBLE'
    assert result.metadata['cancelled']
    assert validate(result, doctors, rules, []).ok


def test_actual_category_objective_against_enumeration(rules):
    doctors = [Doctor('A', id='A'), Doctor('B', id='B')]
    slots = [Slot('a', '2027-02-01', 'SEMAINE', '19:00', '24:00'),
             Slot('b', '2027-02-08', 'SEMAINE', '19:00', '24:00'),
             Slot('c', '2027-02-20', 'SAMEDI', '14:00', '24:00'),
             Slot('d', '2027-02-27', 'SAMEDI', '14:00', '24:00')]
    best = None
    for choices in itertools.product(['A', 'B'], repeat=4):
        global_cost = sum(abs(choices.count(d.id) - 2) for d in doctors)
        category_cost = sum(abs(sum(choices[i] == d.id and slots[i].category == cat for i in range(4)) - 1)
                            for d in doctors for cat in ['SEMAINE', 'SAMEDI'])
        score = (global_cost, category_cost)
        best = min(best, score) if best is not None else score
    result = solve(Plan(slots[0].day, slots[-1].day, slots), doctors, rules, [])
    stages = {s['objective']: s for s in result.metadata['stages']}
    assert (stages['Charge globale']['value'], stages['Catégories']['value']) == (best[0] * 1000, best[1] * 1000)
    assert stages['Catégories']['status'] == 'OPTIMAL'


def test_validated_statistics_frozen_when_doctor_changes(tmp_path, rules):
    s = Slot('s', '2030-02-01', 'SEMAINE', '19:00', '24:00')
    with Project(tmp_path / 'p.gardavu', create=True) as project:
        doctors = [Doctor('A', id='A'), Doctor('B', id='B')]
        for d in doctors:
            project.save_doctor(d)
        project.save_rules(rules)
        validated = project.validate_plan(Plan(s.day, s.day, [s], {'s': ['A']}))
        doctors[0].coefficient = .1
        project.save_doctor(doctors[0])
        rows = statistics(validated, project.doctors())
        assert {r['cible'] for r in rows} == {.5}


def test_complete_recent_history_compensates_without_newcomer_debt(rules):
    doctors = [Doctor('A', id='A'), Doctor('B', id='B'),
               Doctor('Arrivant', id='C', participation=[Span('2027-02-01')])]
    past = [Record(Slot('old1', '2027-01-01', 'SEMAINE', None, None), 'A'),
            Record(Slot('old2', '2027-01-08', 'SEMAINE', None, None), 'A')]
    now = Slot('now', '2027-02-01', 'SEMAINE', '19:00', '24:00')
    result = solve(Plan(now.day, now.day, [now]), doctors, rules, past, history_complete=True)
    assert result.assignments['now'] == ['B']
    assert validate(result, doctors, rules, past, True).ok
