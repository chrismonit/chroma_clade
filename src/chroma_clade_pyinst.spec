# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['gui.py'],
             pathex=['/Users/cmonit1/Desktop/coloured_trees/chroma_clade/src'],
             binaries=[],
             datas=[('title.png', '.'), ('tree.png', '.'), ('col.tree.png', '.'), ('default_colour.csv', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['altgraph', 'certifi', 'chardet', 'cycler', 'DendroPy', 'idna', 'kiwisolver', 'macholib', 'matplotlib', 'numpy', 'pandas', 'patsy', 'pyparsing', 'PyPDF2', 'python-dateutil', 'pytz', 'requests', 'scikit-learn', 'scipy', 'setuptools', 'six', 'sklearn', 'statsmodels', 'tkcolorpicker', 'urllib3'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='chroma_clade_pyinst',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='tree.icns')
app = BUNDLE(exe,
             name='chroma_clade_pyinst.app',
             icon='tree.icns',
             bundle_identifier=None)
