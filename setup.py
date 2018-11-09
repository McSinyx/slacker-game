#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='slacker-game',
    version='2.0.2',
    description='A clone of the arcade game Stacker',
    long_description=long_description,
    url='https://github.com/McSinyx/slacker-game',
    author='Clint Herron',
    maintainer='Nguyễn Gia Phong',
    maintainer_email='vn.mcsinyx@gmail.com',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Games/Entertainment :: Arcade'],
    keywords='stacker arcade-game pygame-application',
    packages=['slacker_game'],
    install_requires=['pygame'],
    package_data={'slacker_game': ['VT323-Regular.ttf', 'icon.png']},
    entry_points={'gui_scripts': ['slacker-game = slacker_game:main']})
