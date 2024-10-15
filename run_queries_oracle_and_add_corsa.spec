# -*- mode: python ; coding: utf-8 -*-

# =============================================================================
#
# @package    stn_sxo_uitzetten
# @container  stn_sxo_uitzetten
# @name       run_queries_oracle_and_add_corsa.spec
# @purpose    pyinstaller spec file
# @version    v0.0.1  2022-04-29
# @author     pierre@amultis.dev
# @copyright  (C) 2020-2024 Pierre Veelen
#
# =============================================================================

a = Analysis(
    ['run_queries_oracle_and_add_corsa.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['cryptography.hazmat.primitives.kdf.pbkdf2'],
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
    name='run_queries_oracle_and_add_corsa',
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
