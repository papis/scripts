#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import papis.cli
import papis.api
from papis.commands.export import run as export
import os
import shutil
import logging

logger = logging.getLogger('papis-html')
logging.basicConfig(level=logging.INFO)

template_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'data'
)

@click.command()
@papis.cli.query_option()
@click.help_option('-h', '--help')
@click.option(
    '-o', '--out',
    help='Output directory',
    default='bibliography'
)
def main(query, out):
    """
    Create a simple searchable offline html site with your references
    """

    logger.info('Searching in database..'.format(out))
    docs = papis.api.get_documents_in_lib(
        library=papis.api.get_lib_name(),
        search=query
    )

    logger.info('Saving in folder {}'.format(out))
    bibtex_text = export(docs, to_format='bibtex')

    logger.info('template files in {}'.format(template_folder))
    shutil.copytree(
        template_folder,
        out
    )

    bibtex_outfile = os.path.join(out, 'library.bib')
    logger.info('Creating bib file in {}'.format(bibtex_outfile))
    with open(bibtex_outfile, 'w+') as fd:
        fd.write(bibtex_text)

    logger.info('Done!')

if __name__ == "__main__":
    main()
