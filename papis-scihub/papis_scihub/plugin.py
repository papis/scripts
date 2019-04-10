import sys
import click
import click.globals
import scihub
import webbrowser
import logging
import papis.importer
import papis.crossref
import tempfile
import colorama

WARNING_NOTICE = '''\
{c.Style.BRIGHT}{c.Fore.RED}{c.Back.YELLOW}
----------------------------------------------------------------------------
|                            WARNING NOTICE:                               |
----------------------------------------------------------------------------
{c.Back.BLACK}

This script uses the platform SCIHUB, which may or MAY NOT be in conflict with
local laws in your country. Use it at your own risk, the author bears no
responsibility.

----------------------------------------------------------------------------
{c.Style.RESET_ALL}
'''.format(c=colorama)
class Importer(papis.importer.Importer):

    def __init__(self, **kwargs):
        papis.importer.Importer.__init__(self, name='scihub', **kwargs)
        self.doi = None

    @classmethod
    def match(cls, uri):
        try:
            papis.doi.validate_doi(uri)
        except ValueError:
            return None
        else:
            return Importer(uri=uri)

    def fetch(self):
        doi_imp = papis.importer.get_importer_by_name('doi').match(self.uri)
        if doi_imp is not None:
            if doi_imp.ctx.data:
                self.ctx.data = doi_imp.ctx.data
            if doi_imp.ctx.files:
                self.ctx.files = doi_imp.ctx.files
                return
        self.get_files()

    def get_files(self):
        self.logger.warning(WARNING_NOTICE)
        sh = scihub.SciHub()
        try:
            res = sh.fetch(self.uri)
        except scihub.CaptchaNeededException:
            curl = sh.get_captcha_url()
            assert(curl is not None)
            assert(curl is not '')
            self.logger.warning('You have to solve the catcha in ' + curl)
            webbrowser.open(curl)
            res = sh.fetch(self.uri)
        except scihub.DocumentUrlNotFound:
            self.logger.error(
                'Sorry, it does not appear to be possible to find and url'
                ' for the given document using scihub'
            )
        else:
            assert(res is not None)
            assert(res.get('url') is not None)
            assert(res.get('pdf') is not None)
            out = tempfile.mktemp(suffix='.pdf')
            self.logger.info('writing file in: {0}'.format(out))
            with open(out, 'wb+') as fd:
                fd.write(res['pdf'])
            self.ctx.files = [out]
