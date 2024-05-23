# -*- mode: python ; coding: utf-8 -*-

# =============================================================================
#
# @package    stn_sxo_uitzetten
# @container  create_pdf_from_csv
# @name       create_pdf_from_csv.spec
# @purpose    pyinstaller spec file
# @version    v0.0.1  2022-04-29
# @author     pierre@amultis.dev
# @copyright  (C) 2020-2024 Pierre Veelen
#
# =============================================================================

a = Analysis(
    ['create_pdf_from_csv.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='create_pdf_from_csv',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
