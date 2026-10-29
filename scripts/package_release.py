"""Archive portable : logiciel, notices et modèles d'import."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description='Assembler les archives de GARDAVU')
    parser.add_argument('--dist-dir', default='dist', help='Dossier contenant le nouvel exécutable')
    args = parser.parse_args()
    destination = ROOT / args.dist_dir
    exe = destination / 'GARDAVU.exe'
    paths = [exe, ROOT / 'README.md', ROOT / 'LICENSE', ROOT / 'THIRD_PARTY_NOTICES.md',
             *list((ROOT / 'docs').glob('*.md')), *list((ROOT / 'templates').glob('*.xlsx')),
             *[p for p in (ROOT / 'licenses').rglob('*') if p.is_file()]]
    archive = destination / 'GARDAVU-portable.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in paths:
            name = 'GARDAVU.exe' if path == exe else path.relative_to(ROOT).as_posix()
            z.write(path, name)
    source_archive = destination / 'GARDAVU-sources.zip'
    source_paths = [*[p for p in ROOT.glob('*') if p.is_file() and p.suffix in ('.py', '.toml', '.txt', '.md', '.spec', '.ps1')], ROOT / 'LICENSE', ROOT / '.gitignore']
    for name in ('gardavu', 'tests', 'scripts', 'docs', 'templates', 'licenses'):
        source_paths.extend(p for p in (ROOT / name).rglob('*')
                            if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith('.lock'))
    with zipfile.ZipFile(source_archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in source_paths:
            z.write(path, path.relative_to(ROOT).as_posix())
    metadata = {}
    for path in (exe, archive, source_archive):
        metadata[path.name] = {'bytes': path.stat().st_size, 'MiB': round(path.stat().st_size / 1048576, 2),
                               'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    (destination / 'distribution.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
