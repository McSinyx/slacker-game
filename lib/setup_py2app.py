"""
Script for building the example.

Usage:
    python setup.py py2app
"""
from setuptools import setup

NAME = 'Slacker'
VERSION = '1.2'

plist = dict(
    CFBundleIconFile='Slacker.icns',
    CFBundleName=NAME,
    CFBundleShortVersionString=VERSION,
    CFBundleGetInfoString=' '.join([NAME, VERSION]),
    CFBundleExecutable=NAME,
    CFBundleIdentifier='pyweek.4.slacker',
)

setup(
    data_files=['../data'],
    app=[
        dict(script="Slacker.py", plist=plist),
    ],
    setup_requires=["py2app"],
)
