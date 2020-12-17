# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.rst') as fd:
    long_description = fd.read()

setup(
    name='papis-html',
    version='0.1',
    author='Alejandro Gallo',
    author_email='aamsgallo@gmail.com',
    license='GPLv3',
    url='https://github.com/papis/scripts/tree/master/papis-html',
    install_requires=[
        "papis>=0.11.1",
        "click",
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
    description='Create a simple searchable offline html '
                'site with your references',
    long_description=long_description,
    keywords=[
        'papis', 'html', 'bibtex', 'javascript'
        'management', 'cli', 'biliography'
    ],
    package_data=dict(
        papis_html=[
            "data/css/bootstrap.min.css",
            "data/index.html",
            "data/js/jquery.min.js",
            "data/js/bibtex_js.js",
        ]
    ),
    entry_points={
        'papis.command': 'html=papis_html:main'
    },
    packages=[
        'papis_html'
    ],
    platforms=['linux', 'osx'],
)
