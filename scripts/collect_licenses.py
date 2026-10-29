"""Collecter versions et textes réellement installés, sans accès réseau."""
from importlib.metadata import distributions
from pathlib import Path
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / 'licenses'
    folder.mkdir(exist_ok=True)
    rows = []
    frozen = []
    for dist in sorted(distributions(), key=lambda d: d.metadata['Name'].casefold()):
        name, version = dist.metadata['Name'], dist.version
        frozen.append(f'{name}=={version}')
        texts = []
        for file in dist.files or []:
            if '.dist-info' in str(file) and any(token in file.name.lower() for token in ('license', 'licence', 'copying', 'notice', 'authors')):
                source = Path(dist.locate_file(file))
                if source.is_file():
                    target = folder / name / str(file).split('.dist-info/', 1)[-1].replace('\\', '/')
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
                    texts.append(str(target.relative_to(ROOT)))
        lic = dist.metadata.get('License-Expression') or dist.metadata.get('License') or ', '.join(v for v in dist.metadata.get_all('Classifier', []) if v.startswith('License ::'))
        rows.append({'name': name, 'version': version, 'license': lic, 'files': texts})
    # Le runtime embarqué comprend Python et Tcl/Tk, même si ce ne sont pas des distributions pip.
    python_dir = Path(sys.base_prefix)
    for source in [python_dir / 'LICENSE.txt', *list((python_dir / 'tcl').glob('*/license.terms'))]:
        if source.is_file():
            target = folder / 'Python-Tcl-Tk' / source.parent.name / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    (ROOT / 'requirements-lock.txt').write_text('\n'.join(frozen) + '\n', encoding='utf-8')
    (folder / 'manifest.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Dépendances réellement utilisées', '', f'Environnement de construction : Python {sys.version.split()[0]}, Windows x64.', '',
             'Les textes fournis par les distributions sont dans le dossier licenses/.',
             f'Licence du programme original : {(ROOT / "LICENSE").read_text(encoding="utf-8").splitlines()[0]} (LICENSE).',
             'Les composants tiers ci-dessous conservent leurs licences propres.',
             'OR-Tools : Apache-2.0 ; openpyxl : MIT ; Python : PSF ; Tcl/Tk : licence BSD historique.',
             'PyInstaller : GPL-2.0-or-later avec exception de distribution des programmes construits.',
             'Pytest et PyInstaller sont des outils de développement, non nécessaires sur le poste destinataire.', '', '| Paquet | Version | Licence déclarée |', '|---|---|---|']
    for row in rows:
        license_text = (row['license'] or 'Consulter le texte fourni').splitlines()[0]
        lines.append(f"| {row['name']} | {row['version']} | {license_text.replace('|', '/')} |")
    lines += ['', 'Références consultées pendant le développement :',
              '- https://pypi.org/project/ortools/9.15.6755/',
              '- https://openpyxl.readthedocs.io/en/stable/',
              '- https://pyinstaller.org/en/stable/license.html',
              '- https://docs.python.org/3/license.html', '']
    (ROOT / 'THIRD_PARTY_NOTICES.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
