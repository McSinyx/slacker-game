#!/usr/bin/env python
from setuptools import setup

with open('README.txt') as f:
    long_description = f.read()

setup(
    name='slacker-game',
    version='1.3.1',
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
    install_requires=['pygame'],
    data_files=[('data/*', ['slacker-game'])],
    scripts=['slacker-game'])
