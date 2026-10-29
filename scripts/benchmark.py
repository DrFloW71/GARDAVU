"""Mesure reproductible du semestre demandé avec contrôle indépendant."""
from datetime import date
import json
from pathlib import Path
import platform
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gardavu.calendar import generate_slots
from gardavu.demo import configured_rules, demo_doctors, demo_records
from gardavu.domain import Plan, dumps
from gardavu.solver import solve
from gardavu.targets import statistics
from gardavu.validation import validate

folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('artifacts/benchmark')
folder.mkdir(parents=True, exist_ok=True)
doctors, rules = demo_doctors(), configured_rules(30)
if '--weight-first' in sys.argv:
    doctors[0].coefficient = float(sys.argv[sys.argv.index('--weight-first') + 1])
    doctors[0].check()
slots = generate_slots(date(2026, 11, 1), date(2027, 4, 30), rules)
history = demo_records(doctors, rules) if '--history' in sys.argv else []
result = solve(Plan('2026-11-01', '2027-04-30', slots), doctors, rules, history)
report = validate(result, doctors, rules, history)
rows = statistics(result, doctors, history)
data = {'platform': platform.platform(), 'python': sys.version, 'period': [result.start, result.end],
        'doctors': len(doctors), 'slots': len(slots), 'required': sum(s.required for s in slots),
        'assigned': sum(map(len, result.assignments.values())), 'status': result.solver_status,
        'errors': report.errors, 'warnings': report.warnings, 'min_total': min(r['total'] for r in rows),
        'max_total': max(r['total'] for r in rows), 'metadata': result.metadata, 'statistics': rows}
(folder / 'benchmark.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
(folder / 'plan.json').write_text(dumps(result), encoding='utf-8')
print(json.dumps({k: v for k, v in data.items() if k not in ('statistics', 'metadata')}, ensure_ascii=True))
raise SystemExit(0 if report.ok else 1)
