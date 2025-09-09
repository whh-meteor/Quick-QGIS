# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_dynamic_libs

binaries = []
binaries += collect_dynamic_libs('tables')


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=[('E:\\Software\\QGIS\\apps\\qgis\\plugins', 'qgis\\plugins'), ('E:\\Software\\QGIS\\apps\\Python312\\Lib\\site-packages\\PyQt5\\*.pyd', 'PyQt5'), ('E:\\Software\\QGIS\\apps\\qt5\\plugins\\styles', 'PyQt5\\Qt\\plugins\\styles'), ('E:\\Software\\QGIS\\apps\\qt5\\plugins\\iconengines', 'PyQt5\\Qt\\plugins\\iconengines'), ('E:\\Software\\QGIS\\apps\\qt5\\plugins\\imageformats', 'PyQt5\\Qt\\plugins\\imageformats'), ('E:\\Software\\QGIS\\apps\\qt5\\plugins\\platforms', 'PyQt5\\Qt\\plugins\\platforms'), ('E:\\Software\\QGIS\\apps\\qt5\\plugins\\platformthemes', 'PyQt5\\Qt\\plugins\\platformthemes'), ('ui', 'ui')],
    hiddenimports=['pyproj'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
