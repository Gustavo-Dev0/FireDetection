# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['f:/SEMESTRE_9/CG/Proyecto/App/interfaz_app/interface_app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Python\\Python310\\Lib\\site-packages\\customtkinter', 'customtkinter/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
a.datas += [("F:\SEMESTRE_9\CG\Proyecto\App\interfaz_app\img\add-folder.png", "App/interfaz_app/img/add-folder.png", "DATA"), ("F:\SEMESTRE_9\CG\Proyecto\App\interfaz_app\img\add-list.png", "App/interfaz_app/img/add-list.png", "DATA"), ("F:\SEMESTRE_9\CG\Proyecto\App\interfaz_app\model\cnn_model_v1.h5", "App/interfaz_app/model/cnn_model_v1.h5", "DATA")]
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='interface_app',
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
