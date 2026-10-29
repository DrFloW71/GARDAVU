from dataclasses import asdict
from tkinter import ttk
import tkinter as tk

import pytest

from gardavu.domain import Doctor
from gardavu.storage import Project
from gardavu.ui import App, Form
from gardavu.ui_theme import PALETTES, messagebox

pytestmark = pytest.mark.gui


def contrast(first, second):
    def luminance(value):
        components = [int(value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in components]
        return sum(a * b for a, b in zip(linear, (.2126, .7152, .0722)))
    a, b = sorted((luminance(first), luminance(second)))
    return (b + .05) / (a + .05)


@pytest.mark.parametrize('mode', ['light', 'dark'])
def test_palette_text_remains_readable(mode):
    c = PALETTES[mode]
    for foreground, background in [(c['text'], c['surface']), (c['muted'], c['bg']),
                                  (c['selected_text'], c['selected']), ('#ffffff', c['accent']),
                                  (c['danger'], c['bg']), (c['warning'], c['warning_bg'])]:
        assert contrast(foreground, background) >= 4.5


def test_theme_persists_and_keeps_in_progress_form_and_data(tmp_path, rules):
    app = App()
    app.withdraw()
    path = tmp_path / 'Apparence.gardavu'
    try:
        project = Project(path, create=True)
        project.save_rules(rules)
        project.save_doctor(Doctor('Élise', id='A', coefficient=2))
        app.set_project(project)
        before = [asdict(d) for d in project.doctors()]
        app.doctor_tree.selection_set('A')
        app.edit_weight()
        form = next(w for w in app.winfo_children() if isinstance(w, Form))
        form.values['coefficient'].delete(0, 'end')
        form.values['coefficient'].insert(0, '2,5')
        app.set_theme('dark')
        assert app.theme_choice.get() == 'Sombre'
        assert form.cget('background') == PALETTES['dark']['bg']
        assert form.values['coefficient'].get() == '2,5'
        assert app.doctor_tree.selection() == ('A',)
        assert project.meta('ui_preferences')['theme'] == 'dark'
        app.set_theme('light')
        assert form.values['coefficient'].get() == '2,5'
        app.set_theme('dark')
        assert [asdict(d) for d in project.doctors()] == before
        assert form.save_button.master == form.footer and form.footer.master == form
        assert form.save_button.winfo_manager() == 'pack'
        form.destroy()
        project.close()
        app.project = None
        app.set_theme('light', persist=False)
        app.set_project(Project(path))
        assert app.theme.mode == 'dark'
        assert app.doctor_tree.item('A', 'values')[1] == '×2'
    finally:
        app.close()


def test_navigation_search_and_numeric_sort_keep_identity(tmp_path, rules):
    app = App()
    app.withdraw()
    try:
        project = Project(tmp_path / 'Recherche.gardavu', create=True)
        project.save_rules(rules)
        project.save_doctor(Doctor('Élise', id='A', coefficient=2, aliases=['Remplaçante']))
        project.save_doctor(Doctor('Élise', id='B', coefficient=10))
        app.set_project(project)
        app.navigation['Médecins et absences'].invoke()
        app.update()
        assert app.nb.select() == str(app.tabs['Médecins et absences'])
        assert app.page_heading.cget('text') == 'Médecins et absences'
        app.doctor_search.set('elise')
        assert len(app.doctor_tree.get_children()) == 2
        app.doctor_tree.selection_set('A')
        app.doctor_tree.sort_column(1)
        assert app.doctor_tree.get_children() == ('A', 'B')
        app.doctor_tree.sort_column(1)
        assert app.doctor_tree.get_children() == ('B', 'A')
        assert app.doctor_tree.selection() == ('A',)
        app.doctor_search.set('remplacante')
        assert app.doctor_tree.get_children() == ('A',)
        app.doctor_search.set('inconnu')
        assert not app.doctor_tree.get_children()
        assert app.doctor_tree.empty_label.winfo_manager() == 'place'
        app.doctor_search.set('B')
        assert app.doctor_tree.get_children() == ('B',)
        assert len(project.doctors()) == 2
    finally:
        app.close()


@pytest.mark.parametrize('answer,expected', [('Non', False), ('Oui', True)])
def test_confirmation_in_dark_mode_retains_explicit_answer(answer, expected):
    app = App()
    app.withdraw()
    try:
        app.set_theme('dark')
        def respond():
            dialog = next(w for w in app.winfo_children() if isinstance(w, tk.Toplevel))
            assert dialog.cget('background') == PALETTES['dark']['bg']
            def find(widget):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button) and child.cget('text') == answer:
                        return child
                    result = find(child)
                    if result is not None:
                        return result
            find(dialog).invoke()
        app.after(20, respond)
        assert messagebox.askyesno('Confirmer', 'Appliquer cette action fictive ?', parent=app) is expected
    finally:
        app.close()
