.. image:: https://badge.fury.io/py/papis-html.svg
    :target: https://badge.fury.io/py/papis-html

Papis-HTML
==========

::

  Usage: papis-html [OPTIONS] [QUERY]

    Create a simple searchable offline html site with your references

  Options:
    -h, --help  Show this message and exit.
    --out TEXT  Output directory

For instance, doing

::

  papis html einstein -o einstein-papers

will get you a directory ``einstein-papers`` with a website inside.

You can find an example in
`here <https://papis.github.io/papis-html/einstein/>`_.

Acknowledgements
================

This is a simple application of the very nice library
`bibtex-js <https://github.com/pcooksey/bibtex-js>`_.

