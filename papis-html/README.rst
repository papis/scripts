.. image:: https://badge.fury.io/py/papis-html.svg
    :target: https://badge.fury.io/py/papis-html

papis-html
==========

For instance, doing

.. code:: sh

    papis html einstein -o einstein-papers

will get you a directory ``einstein-papers`` with a website inside. This website
uses local files, so may not work directly when opened in a modern browser
(due to XSS precautions). You can start a simple web server in the generated
directory with

.. code:: sh

    python -m http.server -d einstein-papers -b 127.0.0.1 8000
    firefox 127.0.0.1:8000

You can find an example `here <https://papis.github.io/papis-html/einstein/>`__.

Acknowledgements
================

This is a simple application of the very nice library
`bibtex-js <https://github.com/pcooksey/bibtex-js>`_.

