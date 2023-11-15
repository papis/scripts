from urllib.parse import urlparse
from typing import Optional
from requests.exceptions import RequestException

import doi
import papis.downloaders
from bs4 import BeautifulSoup

import colorama

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
    bb=colorama.Back.BLACK + colorama.Fore.WHITE,
    ns=colorama.Style.RESET_ALL,
    rb=colorama.Back.RED,
)

BASE_URLS = (f"http://sci-hub.{tld}" for tld in ["ee","se","st","ru"])

class Downloader(papis.downloaders.Downloader):
    def __init__(self, uri: str) -> None:
        self.logger.warning(WARNING_NOTICE)
        papis.downloaders.Downloader.__init__(self, uri=uri, name="sci-hub")
        self.expected_document_extension = "pdf"
        self.priority = 1
        self._get_active_server_url()
        self.doi = _extract_doi(uri)
        self._body = self.session.get(
            f"{self.base_url}/{self.doi}",
            verify=False
        )
        self.bibtex_data = ""

    @classmethod
    def match(cls, url: str) -> Optional[papis.downloaders.Downloader]:
        try:
            _extract_doi(url)
            return Downloader(url)
        except (RequestException, ValueError):
            return None

    def _get_active_server_url(self) -> None:
        for base_url in BASE_URLS:
            if self._ping_server(base_url):
                self.base_url = base_url
                return
        raise RequestException("No Sci-Hub servers can be pinged")

    def _ping_server(self, base_url: str) -> bool:
        try:
            ping = self.session.get(base_url, timeout=1, verify=False)
        except RequestException:
            return False

        if ping.status_code != 200:
            self.logger.error(f"server {base_url} is down")
            return False

        self.logger.debug(f"server {base_url} is up")
        return True

    def get_doi(self) -> Optional[str]:
        return self.doi

    def get_document_url(self) -> Optional[str]:
        soup = BeautifulSoup(self._body.content, "html.parser")
        iframe = soup.find("iframe")
        if not iframe:
            return None

        src = iframe.get("src")
        if src.startswith("//"):
            src = f"https:{src}"
        return src

    def download_bibtex(self) -> None:
        self.bibtex_data = self.session.get(
            f"https://doi.org/{self.doi}",
            headers={"accept": "application/x-bibtex"}
        ).text


def _extract_doi(url: str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.netloc:
        if "doi.org" in parsed_url.netloc:
            doi_ = doi.find_doi_in_text(url)
    else:
        doi_ = url
    try:
        doi.validate_doi(doi_)
        return doi_
    except ValueError as err:
        raise ValueError(
            f"Cannot extract a valid DOI from the provided URL: {url}") from err
