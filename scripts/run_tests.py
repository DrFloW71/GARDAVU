"""Suite métier et scénarios GUI isolés, sans réessai ni masquage des échecs.

Chaque scénario d'interface démarre un seul interpréteur Tk, comme l'exécutable.
Les réinitialisations répétées de Tk dans un même processus Windows sont évitées.
"""
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
from uuid import uuid4
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
folder = ROOT / 'artifacts' / f"tests-{datetime.now():%Y%m%d-%H%M%S}-{uuid4().hex[:6]}"
folder.mkdir(parents=True)
base = [sys.executable, '-m', 'pytest']
collection = subprocess.run([*base, '--collect-only', '-q', '-m', 'gui'], cwd=ROOT,
                            capture_output=True, text=True, encoding='utf-8', errors='replace')
if collection.returncode:
    print(collection.stdout + collection.stderr)
    raise SystemExit(collection.returncode)
nodes = [line.strip() for line in collection.stdout.splitlines() if line.startswith('tests/') and '::' in line]
if not nodes:
    raise SystemExit("Aucun scénario d'interface collecté : vérifiez la sortie de pytest.")
requests = [('metier', ['-m', 'not gui']), *[(f'gui-{i:02}', [node]) for i, node in enumerate(nodes, 1)]]
results = []
totals = dict(tests=0, failures=0, errors=0, skipped=0)
for name, selection in requests:
    report = folder / f'{name}.xml'
    run = subprocess.run([*base, '-q', *selection, f'--basetemp={folder / (name + "-temp")}', f'--junitxml={report}'],
                         cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    (folder / f'{name}.log').write_text(run.stdout + run.stderr, encoding='utf-8')
    if report.exists():
        suites = ET.parse(report).getroot().iter('testsuite')
        for suite in suites:
            for key in totals:
                totals[key] += int(suite.get(key, 0))
    results.append(dict(name=name, selection=selection, exit_code=run.returncode))
    print(f"{name}: {'OK' if run.returncode == 0 else 'ECHEC'}", flush=True)
    if run.returncode:
        print(run.stdout + run.stderr, flush=True)
summary = dict(**totals, success=all(r['exit_code'] == 0 for r in results), runs=results)
(folder / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({key: value for key, value in summary.items() if key != 'runs'}), flush=True)
print(str(folder), flush=True)
raise SystemExit(0 if summary['success'] else 1)
