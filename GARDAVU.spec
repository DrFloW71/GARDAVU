# Construction native Windows x64 ; aucune donnée projet embarquée.
from PyInstaller.utils.hooks import collect_dynamic_libs

a = Analysis(
    ['run_gardavu.py'], pathex=['.'],
    binaries=collect_dynamic_libs('ortools'),
    datas=[('LICENSE', '.'), ('THIRD_PARTY_NOTICES.md', '.'), ('licenses', 'licenses'),
           ('gardavu/assets/gardavu.ico', 'gardavu/assets'),
           ('gardavu/assets/gardavu.png', 'gardavu/assets'),
           ('gardavu/assets/handcuffs-sidebar.png', 'gardavu/assets')],
    hiddenimports=['ortools.sat.python.cp_model_helper', 'ortools.util.python.sorted_interval_list'],
    hookspath=[], runtime_hooks=['scripts/runtime_dlls.py'], excludes=['matplotlib', 'scipy', 'IPython', 'pytest'],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name='GARDAVU',
          icon='gardavu/assets/gardavu.ico',
          debug=False, bootloader_ignore_signals=False, strip=False, upx=False,
          console=False, disable_windowed_traceback=False)
