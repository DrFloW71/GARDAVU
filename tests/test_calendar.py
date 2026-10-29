from datetime import date
import pytest
from gardavu.calendar import add_months, calendar_months, easter, generate_slots, holidays, period_end
from gardavu.domain import Rules


def test_period_and_leap():
    assert period_end(date(2026, 11, 1), 6) == date(2027, 4, 30)
    assert add_months(date(2024, 1, 31), 1) == date(2024, 2, 29)
    assert period_end(date(2024, 1, 31), 1) == date(2024, 2, 28)
    assert period_end(date(2026, 11, 15), 6) == date(2027, 5, 14)


def test_six_calendar_months_keep_weekday_threshold_two():
    from math import ceil
    assert ceil(calendar_months(date(2027, 5, 1), date(2027, 10, 31)) / 3) == 2
    assert ceil(calendar_months(date(2026, 11, 1), date(2027, 4, 30)) / 3) == 2
    assert ceil(calendar_months(date(2027, 1, 1), date(2027, 12, 31)) / 3) == 4


def test_official_2026_calendar():
    h = holidays(2026)
    assert h[date(2026, 4, 6)] == ("LUNDI_PAQUES",)
    assert h[date(2026, 5, 14)] == ("ASCENSION",)
    assert h[date(2026, 5, 25)] == ("LUNDI_PENTECOTE",)
    assert sum(map(len, h.values())) == 11
    assert date(2026, 12, 24) not in h and date(2026, 12, 31) not in h
    assert easter(2000) == date(2000, 4, 23)
    assert easter(2038) == date(2038, 4, 25)


def test_holiday_collision_and_weekend(rules):
    saturday = generate_slots(date(2026, 8, 15), date(2026, 8, 15), rules)
    sunday = generate_slots(date(2026, 11, 1), date(2026, 11, 1), rules)
    assert len(saturday) == len(sunday) == 2
    assert all(s.category.startswith("FERIE") for s in saturday + sunday)
    collision = holidays(2008)[date(2008, 5, 1)]
    assert set(collision) == {"TRAVAIL", "ASCENSION"}
    ss = generate_slots(date(2008, 5, 1), date(2008, 5, 1), rules)
    assert len(ss) == 2 and set(ss[0].holidays) == set(collision)


def test_four_weeks_32_and_midnight(rules):
    slots = generate_slots(date(2027, 2, 1), date(2027, 2, 28), rules)
    assert len(slots) == sum(s.required for s in slots) == 32
    assert slots[-1].interval[1] == __import__('datetime').datetime(2027, 3, 1)
    leap = generate_slots(date(2024, 2, 29), date(2024, 2, 29), rules)
    assert leap[0].date == date(2024, 2, 29)


def test_missing_hours_and_confirmation():
    r = Rules()
    with pytest.raises(ValueError, match="Confirmez"):
        generate_slots(date(2027, 2, 1), date(2027, 2, 1), r)
    r.gap_confirmed = True
    with pytest.raises(ValueError, match="Horaires incomplets"):
        generate_slots(date(2027, 2, 1), date(2027, 2, 1), r)


def test_exceptions_and_effective_versions(rules):
    from dataclasses import asdict, replace
    rules.templates.append(replace(rules.templates[0], effective="2027-02-02", start="18:30"))
    slots = generate_slots(date(2027, 2, 1), date(2027, 2, 2), rules)
    assert [s.start for s in slots] == ["19:00", "18:30"]
    rules.date_exceptions["2027-02-01"] = []
    assert len(generate_slots(date(2027, 2, 1), date(2027, 2, 2), rules)) == 1
    rules.holiday_exceptions["2027-02-02"] = {"add": ["PARTICULIER"], "remove": []}
    slots = generate_slots(date(2027, 2, 2), date(2027, 2, 2), rules)
    assert len(slots) == 2 and slots[0].holidays == ("PARTICULIER",)
