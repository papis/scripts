# -*- coding: utf-8 -*-
from setuptools import setup

from papis_bibtex import __version__

with open('README.md') as fd:
    long_description = fd.read()

setup(
    name='papis-bibtex',
    version=__version__,
    author='Alejandro Gallo',
    author_email='aamsgallo@gmail.com',
    license='GPLv3',
    install_requires=[
        "papis>=0.8.2",
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    description='Special bibtex tool for papis',
    long_description=long_description,
    extras_require=dict(
        develop=[
            "sphinx",
            'sphinx-click',
            'sphinx_rtd_theme',
            'pytest',
            'pytest-cov',
        ]
    ),
    keywords=[
        'papis', 'bibtex', 'bibtex',
        'management', 'cli', 'biliography'
    ],
    packages=[
        "papis_bibtex",
    ],
    entry_points={
        'papis.command': [
            'bibtex=papis_bibtex.main:main'
        ],
    },
    platforms=['linux', 'osx'],
)
