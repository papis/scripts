#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import click
import click.globals
import scihub
import papis.commands.add
import webbrowser
import logging

logger = logging.getLogger('papis:scihub')
logging.basicConfig(filename="", level=logging.INFO)

WARNING_NOTICE = '''\
----------------------------------------------------------------------------
                             WARNING NOTICE:
----------------------------------------------------------------------------

This script uses the platform SCIHUB, which may or MAY NOT be in conflict with
local laws in your country. Use it at your own risk, the author bears no
responsibility.

----------------------------------------------------------------------------
'''


def set_default(command, param_name, default):
    for p in command.params:
        if p.name == param_name:
            p.default = default
            return True
    raise Exception(
        'No param {param_name} found in cmd {command}'.format(**locals())
    )


@click.group()
@click.help_option('-h', '--help')
@click.argument('identifier', nargs=1)
@click.option(
    '-o', '--out', help='Path for downloaded document',
    default='output.pdf', nargs=1
)
@click.pass_context
def main(ctx, identifier, out):
    """
    Examples:

      papis scihub 10.1002/andp.19053220607 add -d einstein_papers --name photon_definition

      # Add the document to papis' library
      papis scihub http://physicstoday.scitation.org/doi/10.1063/1.881498 add --name important_paper

      # Save the document in test.pdf
      papis scihub -o test.pdf https://doi.org/10.1016/j.physrep.2016.12.002
    """
    global logger
    click.echo(WARNING_NOTICE)
    sh = scihub.SciHub()
    try:
        res = sh.fetch(identifier)
    except scihub.CaptchaNeededException:
        curl = sh.get_captcha_url()
        assert(curl is not None)
        assert(curl is not '')
        click.echo('You have to solve the catcha in ' + curl)
        webbrowser.open(curl)
        res = sh.fetch(identifier)
    except scihub.DocumentUrlNotFound:
        logging.exception(
            'Sorry, it does not appear to be possible to find and url'
            ' for the given document using scihub'
        )
        sys.exit(0)
    else:
        assert(res is not None)
        assert(res.get('url') is not None)
        assert(res.get('pdf') is not None)
        logger.info('Writing file in: {0}'.format(out))
        with open(out, 'wb+') as fd:
            fd.write(res['pdf'])

    ctx.obj = {
        'path': out,
        'identifier': identifier,
    }


papis_add_cmd = papis.commands.add.cli
papis_add_callback = papis_add_cmd.callback
main.add_command(papis_add_cmd, 'add')
def add(**kwargs):
    logger = logging.getLogger('papis:scihub:add')
    ctx = click.globals.get_current_context()
    kwargs['files'] = [ctx.obj['path']]
    logger.info('files: {0}'.format(kwargs['files']))
    kwargs['from_doi'] = ctx.obj['identifier']
    papis_add_callback(**kwargs)

papis_add_cmd.callback = add


if __name__ == "__main__":
    main()
