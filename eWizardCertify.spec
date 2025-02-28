# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[
        ('C:\\Users\\KC Sean\\Desktop\\PROJECTS\\Commissions\\tryPython_Certificate\\poppler_bin\\Release\\poppler\\Library\\bin\\pdftoppm.exe', 'poppler_bin'), 
        ('C:\\Users\\KC Sean\\Desktop\\PROJECTS\\Commissions\\tryPython_Certificate\\poppler_bin\\Release\\poppler\\Library\\bin\\pdftocairo.exe', 'poppler_bin'),
        ('C:\\Users\\KC Sean\\Desktop\\PROJECTS\\Commissions\\tryPython_Certificate\\poppler_bin\\Release\\poppler\\Library\\bin\\*.dll', 'poppler_bin')
    ],
    datas=[
        ('custom_template', 'custom_template'), 
        ('public/docx', 'public/docx'), 
        ('public/img', 'public/img'), 
        ('public/pdf', 'public/pdf'), 
        ('resources/icons', 'resources/icons'), 
        ('resources/template_img', 'resources/template_img'), 
        ('resources/edit_line.png', 'resources'), 
        ('resources/left-arrows.png', 'resources'), 
        ('resources/logo.ico', 'resources'), 
        ('resources/logo1.ico', 'resources'), 
        ('template', 'template'), 
        ('temporary', 'temporary'), 
        ('View', 'View'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL',
        'docx',
        'pdf2image',
        'docx2pdf',
        'lxml',
        'tkinter',
        'shutil',
        'os',
        're',
        'time',
        'threading',
        'logging',
        'PyPDF2',
        'zipfile',
        'psutil',
        'comtypes'
    ],
    hookspath=[],
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
    name='eCertifyWizard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/logo1.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='eCertify Wizard',
)
