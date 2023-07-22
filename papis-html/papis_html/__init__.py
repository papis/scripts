#! /usr/bin/env python3

import os
import shutil

import click

import papis.cli
import papis.api
import papis.logging
from papis.commands.export import run as export

logger = papis.logging.get_logger("papis_html")

template_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data"
)


@click.command()
@papis.cli.query_argument()
@click.help_option("-h", "--help")
@click.option(
    "-o", "--out",
    help="Output directory",
    default="html"
)
def main(query: str, out: str) -> None:
    """
    Create a simple searchable offline HTML site with your documents
    """
    if os.path.exists(out):
        logger.error("Output directory '%s' already exists.", out)

    logger.info("Searching in database.")
    docs = papis.api.get_documents_in_lib(
        library=papis.api.get_lib_name(),
        search=query
    )

    bibtex_text = export(docs, to_format="bibtex")

    shutil.copytree(template_folder, out)
    logger.info("Template files copied from '%s'.", template_folder)
    logger.info("Saving in folder '%s'.", out)

    bibtex_outfile = os.path.join(out, "papis-html-library.bib")
    with open(bibtex_outfile, "w+") as fd:
        fd.write(bibtex_text)

    logger.info("Created BibTex file: '%s'.", bibtex_outfile)
