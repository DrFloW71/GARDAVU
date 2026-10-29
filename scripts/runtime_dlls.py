"""Chemins des DLL embarquées, avant l'import NumPy/OR-Tools.

NumPy et pandas partagent une DLL MSVC de même nom. PyInstaller la déduplique
dans pandas.libs : les deux répertoires doivent être visibles dès le premier import.
Aucune donnée persistante n'est écrite ici.
"""
import os
from pathlib import Path
import sys

_gardavu_dll_handles = []
if os.name == 'nt' and getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)
    for relative in ('.', 'numpy.libs', 'pandas.libs', 'ortools/.libs'):
        folder = root / relative
        if folder.is_dir():
            _gardavu_dll_handles.append(os.add_dll_directory(str(folder)))
