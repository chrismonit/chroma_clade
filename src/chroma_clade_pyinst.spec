# -*- mode: python -*-

block_cipher = None


a = Analysis(['gui.py'],
             pathex=['/Users/cmonit1/Desktop/coloured_trees/chroma_clade/src'],
             binaries=[],
             datas=[('title.png', '.'), ('tree.png', '.'), ('col.tree.png', '.'), ('default_colour.csv', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='chroma_clade_pyinst',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='tree.icns')
