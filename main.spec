# -*- mode: python ; coding: utf-8 -*-

import os

a = Analysis(
    ['src\\main.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[
        ('src\\*.py', 'src'),  # 打包src下所有py文件
        ('src\\**\\*.py', 'src'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SLES',  # 程序名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
