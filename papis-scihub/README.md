# Papis-SciHub

This [Papis](https://github.com/papis/papis/) plugin provides a Sci-Hub `Importer`.

## Installation

`pip install git+https://github.com/raj-magesh/papis-scihub.git`

## Usage

```bash
papis add [--from scihub] <doi>
```

- The `Importer` corresponding to this plugin is called `scihub`, so the option `--from scihub` will add files only from Sci-Hub.
- DOIs can be provided either as raw strings (e.g. `10.1101/2021.03.21.436284`) or as complete URLs (e.g. `https://doi.org/10.1101/2021.03.21.436284`).

