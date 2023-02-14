# -*- mode: python ; coding: utf-8 -*-

import os
import platform

block_cipher = None

data = [(os.path.join('src', 'data', 'logo.png'), '.'),
        (os.path.join('src', 'data', 'logo.ico'), '.'),
        (os.path.join('src', 'Paint.kv'), '.'),
        ]

if platform.system() == 'Windows':
    icon=os.path.join('src', 'data', 'logo.ico')
else:
    icon=os.path.join('src', 'data', 'logo.png')

a = Analysis(
    [os.path.join('src', 'main.py')],
    pathex=[],
    binaries=[],
    datas=data,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['cv2', 'mkl', 'psutil', 'numpy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Paint',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Paint',
)
