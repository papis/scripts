import doi
import scihub
import webbrowser
import papis.importer
import papis.crossref
import tempfile
import colorama
import warnings
import urllib.request


WARNING_NOTICE = '''
{bb} .+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+. {ns}
{bb}(                                                                 ){ns}
{bb} )                    {rb} WARNING NOTICE {bb}                           \
( {ns}
{bb}(                     ----------------                            ){ns}
{bb} )                                                               ( {ns}
{bb}(  This script uses the platform {rb}SCIHUB{bb}, which may or MAY NOT     \
){ns}
{bb} ) be in conflict with local laws in your country. Use it at     ( {ns}
{bb}(  your own risk, {rb}the author bears no responsibility{bb}.             \
){ns}
{bb} )                                                               ( {ns}
{bb}(                                           papis team            ){ns}
{bb} "+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+" {ns}\
'''.format(
    bb=colorama.Back.BLACK,
    ns=colorama.Style.RESET_ALL,
    rb=colorama.Back.RED,
)


class Importer(papis.importer.Importer):

    def __init__(self, **kwargs):
        papis.importer.Importer.__init__(self, name='scihub', **kwargs)
        self.doi = None

    @classmethod
    def match(cls, uri):
        try:
            doi.validate_doi(uri)
        except ValueError:
            return None
        else:
            return Importer(uri=uri)

    def fetch(self):
        doi_str = (
            doi.find_doi_in_text(self.uri) or
            doi.find_doi_in_text(
                urllib.request.urlopen(self.uri).read().decode('utf-8')
            ) or
            self.uri
        )
        ctx = self.fetch_from_doi(doi_str)
        if ctx:
            if ctx.data:
                self.ctx.data = ctx.data
            if ctx.files:
                self.ctx.files = ctx.files
                return
        self.get_files()

    def fetch_from_doi(self, doi_str):
        doi_imp = papis.importer.get_importer_by_name('doi').match(doi_str)
        if doi_imp is not None:
            self.logger.info('getting data through doi')
            doi_imp.fetch()
            return doi_imp.ctx

    def get_files(self):
        # ignore the https warnings for scihub
        warnings.simplefilter('ignore')
        self.logger.warning(WARNING_NOTICE)
        sh = scihub.SciHub(self.uri)
        try:
            ctx = sh.fetch()
        except scihub.CaptchaNeededException:
            curl = sh.get_captcha_url()
            assert(curl is not None)
            assert(curl is not '')
            self.logger.warning('You have to solve the catcha in ' + curl)
            webbrowser.open(curl)
            ctx = sh.fetch(self.uri)
        except scihub.DocumentUrlNotFound:
            self.logger.error(
                'Sorry, it does not appear to be possible to find and url'
                ' for the given document using scihub'
            )
        else:
            assert(ctx is not None)
            assert(ctx.url is not None)
            assert(ctx.pdf is not None)
            out = tempfile.mktemp(suffix='.pdf')
            self.logger.info('got file from: {0}'.format(ctx.url))
            self.logger.info('writing file in: {0}'.format(out))
            with open(out, 'wb+') as fd:
                fd.write(ctx.pdf)
            self.ctx.files = [out]
            if not self.ctx.data and ctx.doi:
                doi_ctx = self.fetch_from_doi(ctx.doi)
                if doi_ctx.data:
                    self.logger.info('got data from doi {0}'.format(ctx.doi))
                    self.ctx.data = doi_ctx.data
