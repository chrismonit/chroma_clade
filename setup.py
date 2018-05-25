"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""
#import macholib_patch

from setuptools import setup

APP = ['src/gui.py']
DATA_FILES = ['src/dat/default_colour.csv', 'src/pic/tree.gif', 'src/pic/col.tree.gif', 'src/pic/title.gif']
OPTIONS = {}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
