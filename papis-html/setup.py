from setuptools import setup

with open("README.rst") as fd:
    long_description = fd.read()

setup(
    name="papis-html",
    version="0.1",
    author="Alejandro Gallo",
    author_email="aamsgallo@gmail.com",
    license="GPLv3",
    url="https://github.com/papis/scripts/tree/master/papis-html",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: Microsoft",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
    description="Create a simple searchable offline HTML site with your references",
    long_description=long_description,
    keywords=[
        "papis", "html", "bibtex", "javascript"
        "management", "cli", "biliography"
    ],
    install_requires=[
        "papis>=0.13",
    ],
    python_requires=">=3.8",
    extras_require={
        "develop": [
            "flake8-bugbear",
            "flake8-quotes",
            "flake8",
            "mypy>=0.7",
            "pep8-naming",
        ],
    },
    package_data=dict(
        papis_html=[
            "data/css/bootstrap.min.css",
            "data/index.html",
            "data/js/jquery.min.js",
            "data/js/bibtex_js.js",
        ]
    ),
    entry_points={
        "papis.command": [
            "html=papis_html:main"
        ]
    },
    packages=[
        "papis_html"
    ],
    platforms=["linux", "osx", "win32"],
)
