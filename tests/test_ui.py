from datetime import date
import tkinter as tk
from tkinter import ttk
import pytest

from gardavu.calendar import generate_slots
from gardavu.domain import Plan, Rules, Slot
from gardavu.exports import export_excel
from gardavu.storage import Project
from gardavu.ui import App, Form, ImportWizard, parse_spans

pytestmark = pytest.mark.gui


def test_ui_project_plan_filter_and_import_preview(tmp_path, rules, doctors):
    app = App()
    app.withdraw()
    try:
        p = Project(tmp_path / 'Interface été.gardavu', create=True)
        p.save_rules(rules)
        for d in doctors[:2]:
            p.save_doctor(d)
        app.set_project(p)
        a = Slot('a', '2030-02-01', 'SEMAINE', '19:00', '24:00')
        b = Slot('b', '2030-02-09', 'SAMEDI', '14:00', '24:00')
        app.plan = Plan(a.day, b.day, [a, b], {'a': ['DEMO-001'], 'b': ['DEMO-002']})
        app.project.save_draft(app.plan)
        app.refresh()
        app.update()
        assert len(app.planning_tree.get_children()) == 2
        assert len(app.equity_tree.get_children()) == 2
        app.filter_doctor.set(next(k for k, v in app.filter_options.items() if v == 'DEMO-001'))
        app.refresh_plan()
        assert len(app.planning_tree.get_children()) == 1
        assert app.month_grid.winfo_children()
        app.plan.assignments['b'] = ['DEMO-001']
        app.plan.assignments['a'] = []
        app.after_edit('test_controle_modification')
        assert app.plan.solver_status == 'MODEL_INVALID'
        assert 'NON VALIDÉ' in app.plan_status.cget('text')
        app.plan.state = 'VALIDE'
        app.plan.assignments = {'a': ['DEMO-001'], 'b': ['DEMO-002']}
        path = tmp_path / 'export.xlsx'
        export_excel(path, app.plan, doctors[:2])
        from gardavu.imports import read_sheets
        wizard = ImportWizard(app, 'history')
        wizard.withdraw()
        wizard.path = str(path)
        wizard.sheets = read_sheets(path)
        wizard.sheet.set('Planning')
        wizard.header.set('3')
        wizard.build_mapping.__wrapped__(wizard)
        wizard.prepare.__wrapped__(wizard)
        assert len(wizard.preview.records) == 2 and not wizard.preview.errors
        assert not wizard.preview.unresolved
        wizard.destroy()
    finally:
        app.close()


def test_span_entry_inclusive_and_open_end():
    spans = parse_spans('2030-01-01..2030-01-02\n2031-01-01..')
    assert spans[0].contains(date(2030, 1, 2))
    assert not spans[0].contains(date(2030, 1, 3))
    assert spans[1].contains(date(2040, 1, 1))


def test_configure_first_weekday_hours_without_leaving_incomplete_version(tmp_path):
    app = App()
    app.withdraw()
    try:
        project = Project(tmp_path / 'Configuration.gardavu', create=True)
        project.save_rules(Rules(gap_confirmed=True))
        app.set_project(project)
        app.template_tree.selection_set('0')
        buttons = [w for frame in app.tabs['Créneaux et règles'].winfo_children()
                   for w in frame.winfo_children() if isinstance(w, ttk.Button)]
        next(w for w in buttons if w.cget('text') == 'Configurer le créneau').invoke()
        dialog = next(w for w in app.winfo_children() if isinstance(w, Form))
        assert dialog.values['effective'].get() == '1900-01-01'
        for key, value in [('start', '20:00'), ('end', '24:00')]:
            dialog.values[key].delete(0, 'end')
            dialog.values[key].insert(0, value)
        dialog.accept.__wrapped__(dialog)
        rules = project.rules()
        assert len([t for t in rules.templates if t.id == 'soir']) == 1
        slots = generate_slots(date(2026, 11, 2), date(2026, 11, 2), rules)
        assert [(s.start, s.end) for s in slots] == [('20:00', '24:00')]
        # La commande distincte conserve la création d'une nouvelle version datée.
        row = next(str(i) for i, t in enumerate(rules.templates) if t.id == 'soir')
        app.template_tree.selection_set(row)
        app.edit_template(True, new_version=True)
        dialog = next(w for w in app.winfo_children() if isinstance(w, Form))
        assert dialog.values['effective'].get() == date.today().isoformat()
        dialog.destroy()
    finally:
        app.close()


def test_template_pointer_actions_select_the_clicked_row(tmp_path, monkeypatch, rules):
    from types import SimpleNamespace
    app = App()
    app.withdraw()
    try:
        project = Project(tmp_path / 'Menu.gardavu', create=True)
        project.save_rules(rules)
        app.set_project(project)
        app.template_tree.selection_set('0')
        monkeypatch.setattr(app.template_tree, 'identify_row', lambda y: '1' if y == 50 else '')
        opened = []
        monkeypatch.setattr(app, 'edit_template', lambda existing: opened.append(app.template_tree.selection()))
        assert app.configure_template_at(SimpleNamespace(y=50)) == 'break'
        assert opened == [('1',)]
        app.template_tree.selection_set('0')
        popup = []
        monkeypatch.setattr(app.template_menu, 'tk_popup', lambda x, y: popup.append((x, y)))
        monkeypatch.setattr(app.template_menu, 'grab_release', lambda: None)
        app.template_context_menu(SimpleNamespace(y=50, x_root=300, y_root=250))
        assert app.template_tree.selection() == ('1',) and popup == [(300, 250)]
        app.template_menu.invoke(0)
        assert opened == [('1',), ('1',)]
        app.configure_template_at(SimpleNamespace(y=999))
        app.template_context_menu(SimpleNamespace(y=999))
        assert len(opened) == 2 and len(popup) == 1
    finally:
        app.close()
