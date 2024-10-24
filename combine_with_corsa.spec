# -*- mode: python ; coding: utf-8 -*-

# =============================================================================
#
# @package    stn_sxo_uitzetten
# @container  stn_sxo_uitzetten
# @name       combine_with_corsa.spec
# @purpose    pyinstaller spec file
# @version    v0.0.1  2024-10-24
# @author     pierre@amultis.dev
# @copyright  (C) 2020-2024 Pierre Veelen
#
# =============================================================================

a = Analysis(
    ['combine_with_corsa.py'],
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
    name='combine_with_corsa',
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
