from pathlib import Path

import pytest

from gardavu import __author__
from gardavu.ui import App, LicenseDialog
from gardavu.ui_theme import PALETTES

pytestmark = pytest.mark.gui


@pytest.mark.parametrize('mode', ['light', 'dark'])
def test_information_available_without_project_and_during_calculation(mode):
    app = App()
    app.withdraw()
    try:
        app.set_theme(mode)
        app.busy = True
        app.update_actions()
        assert not app.info_button.instate(['disabled'])
        app.info_button.invoke()
        dialog = app.license_dialog
        assert isinstance(dialog, LicenseDialog)
        assert dialog.cget('background') == PALETTES[mode]['bg']
        assert app.grab_current() is dialog and app.project is None
        assert [dialog.notebook.tab(tab, 'text') for tab in dialog.notebook.tabs()] == ['Licence GARDAVU', 'Composants tiers']
        assert 'Toute utilisation, même gratuite' in dialog.notice.cget('text')
        current = dialog.current_text.get('1.0', 'end')
        assert __author__ in current and 'non commerciales' in current
        assert 'préalable, expresse et écrite' in current
        assert 'EN ATTENTE DE VALIDATION' not in current and 'PROPOSITION' not in current
        assert all(w.cget('state') == 'disabled' for w in (dialog.current_text, dialog.third_party_text))
        assert app.about() is dialog
        # Le sélecteur permet aussi de lire un texte complet, pas seulement sa synthèse.
        document = next(s for s in dialog.third_party_choice['values'] if s.startswith('licenses/openpyxl/'))
        dialog.third_party_choice.set(document)
        dialog.third_party_choice.event_generate('<<ComboboxSelected>>')
        app.update()
        root = Path(__file__).resolve().parents[1]
        expected = (root / document).read_text(encoding='utf-8-sig', errors='replace')
        assert dialog.third_party_text.get('1.0', 'end').strip() == expected.strip()
        assert current.strip() == (root / 'LICENSE').read_text(encoding='utf-8').strip()
        assert 'MIT' in (root / document).read_text(encoding='utf-8-sig', errors='replace')
        dialog.destroy()
        assert app.grab_current() is None
    finally:
        app.busy = False
        app.close()


def test_information_icon_remains_bottom_right_with_long_status():
    app = App()
    try:
        app.geometry('1040x720+10000+10000')
        app.status.configure(text='Sauvegarde créée : ' + 'dossier très long/' * 100)
        app.update()
        button = app.info_button
        assert button.winfo_ismapped()
        right_gap = app.winfo_rootx() + app.winfo_width() - button.winfo_rootx() - button.winfo_width()
        assert 0 <= right_gap <= 24
        assert button.winfo_rooty() + button.winfo_height() <= app.winfo_rooty() + app.winfo_height()
        button.invoke()
        app.update()
        dialog = app.license_dialog
        assert dialog.winfo_ismapped()
        dialog.destroy()
    finally:
        app.close()
