from dataclasses import asdict
import tkinter as tk
from tkinter import ttk

import pytest

from gardavu.domain import Doctor, Plan, Slot
from gardavu.storage import Project
from gardavu.ui import App
from gardavu.ui_theme import PALETTES

pytestmark = pytest.mark.gui


def setup_equity(app, tmp_path, rules):
    project = Project(tmp_path / 'Détail équité.gardavu', create=True)
    project.save_rules(rules)
    doctors = [Doctor('Autre', id='A'), Doctor('Pondéré', id='B', coefficient=2)]
    for doctor in doctors:
        project.save_doctor(doctor)
    app.set_project(project)
    slot = Slot('noel', '2027-12-25', 'FERIE_JOUR', '08:00', '19:00', holidays=('NOEL',))
    app.plan = Plan(slot.day, slot.day, [slot], {slot.id: ['B']})
    app.plan.state = 'VALIDE'
    app.plan.metadata.update(doctors_snapshot=[asdict(d) for d in doctors], validated_rules=asdict(rules))
    # Le détail doit conserver la fiche de validation, comme le tableau d'équité.
    project.save_doctor(Doctor('Fiche actuelle', id='B', coefficient=1))
    app.refresh_plan()
    return next(w for frame in app.tabs['Équité et exports'].winfo_children()
                for w in frame.winfo_children() if isinstance(w, ttk.Button)
                and w.cget('text') == 'Détail du médecin sélectionné')


@pytest.mark.parametrize('mode', ['light', 'dark'])
def test_button_opens_selected_doctor_details_with_validated_values(tmp_path, rules, monkeypatch, mode):
    app = App()
    app.withdraw()
    try:
        button = setup_equity(app, tmp_path, rules)
        app.set_theme(mode)
        opened = []
        monkeypatch.setattr('gardavu.ui.messagebox.showinfo', lambda title, message, **kwargs: opened.append((title, message, kwargs)))
        app.equity_tree.sort_column(0)
        app.equity_tree.selection_set('B')
        button.invoke()
        assert len(opened) == 1
        title, text, options = opened[0]
        assert title == 'Détail — Pondéré' and options['parent'] is app
        assert 'Pondération : ×2' in text and '25/12/2027' in text
        assert '2027-12 : 1' in text and 'attribué 1' in text
        assert 'NOEL' in text and 'aucune occurrence connue' in text
        assert app.equity_detail.get('1.0', 'end').strip() == text
        assert app.plan.assignments == {'noel': ['B']}
        assert app.project.doctors()[1].coefficient == 1
    finally:
        app.close()


@pytest.mark.parametrize('selection', [(), ('A', 'B')], ids=['aucun', 'plusieurs'])
def test_detail_requires_one_selection_with_explicit_feedback(tmp_path, rules, monkeypatch, selection):
    app = App()
    app.withdraw()
    try:
        button = setup_equity(app, tmp_path, rules)
        app.equity_tree.selection_set(selection)
        errors, opened = [], []
        monkeypatch.setattr('gardavu.ui.messagebox.showerror', lambda title, message, **kwargs: errors.append(message))
        monkeypatch.setattr('gardavu.ui.messagebox.showinfo', lambda *args, **kwargs: opened.append(args))
        button.invoke()
        assert len(errors) == 1 and 'un seul médecin' in errors[0]
        assert not opened
        assert app.plan.assignments == {'noel': ['B']}
    finally:
        app.close()


def test_detail_is_visible_in_a_dialog_at_small_window_size(tmp_path, rules):
    app = App()
    observed = {}
    try:
        button = setup_equity(app, tmp_path, rules)
        app.set_theme('dark')
        app.select_page('Équité et exports')
        app.geometry('1040x720+10000+10000')
        app.update()
        app.equity_tree.selection_set('B')
        def inspect_and_close():
            dialog = next((w for w in app.winfo_children() if isinstance(w, tk.Toplevel)), None)
            if dialog is None:
                return
            try:
                observed.update(title=dialog.title(), mapped=bool(dialog.winfo_ismapped()),
                                modal=app.grab_current() is dialog, background=dialog.cget('background'))
                pending, texts = [dialog], []
                while pending:
                    widget = pending.pop()
                    pending.extend(widget.winfo_children())
                    if isinstance(widget, tk.Text):
                        texts.append(widget.get('1.0', 'end'))
                observed['text'] = '\n'.join(texts)
            finally:
                dialog.destroy()
        app.after(80, inspect_and_close)
        button.invoke()
        assert observed['title'] == 'Détail — Pondéré'
        assert observed['mapped'] and observed['modal']
        assert observed['background'] == PALETTES['dark']['bg']
        assert 'Pondération : ×2' in observed['text']
    finally:
        app.close()
