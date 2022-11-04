from urllib.parse import urlparse

import doi
import papis.downloaders
from bs4 import BeautifulSoup


BASE_URLS = ("http://sci-hub.ee",)


class Downloader(papis.downloaders.Downloader):
    def __init__(self, uri: str) -> None:
        papis.downloaders.Downloader.__init__(self, uri=uri, name="sci-hub")
        self.expected_document_extension = "pdf"
        self.priority = 1

        try:
            self._get_active_server_url()
        except Exception as e:
            raise e

        self.doi = _extract_doi(uri)
        self._body = self.session.get(
            f"{self.base_url}/{self.doi}",
            verify=False
        )

    @classmethod
    def match(cls, url: str) -> papis.downloaders.Downloader | None:
        try:
            _extract_doi(url)
            return Downloader(url)
        except Exception:
            return None

    def _get_active_server_url(self) -> None:
        for base_url in BASE_URLS:
            if self._ping_server(base_url):
                self.base_url = base_url
                return
        raise Exception("No Sci-Hub servers can be pinged")

    def _ping_server(self, base_url: str) -> bool:
        try:
            ping = self.session.get(base_url, timeout=1, verify=False)
            if ping.status_code != 200:
                self.logger.error(f"server {base_url} is down")
                return False
            else:
                self.logger.debug(f"server {base_url} is up")
                return True
        except Exception:
            return False

    def get_doi(self) -> str | None:
        return self.doi

    def get_document_url(self) -> str | None:
        s = BeautifulSoup(self._body.content, "html.parser")
        iframe = s.find("iframe")
        if iframe:
            src = iframe.get("src")
            if src.startswith("//"):
                src = f"https:{src}"
            return src
        else:
            return None

    def download_bibtex(self) -> str:
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
    except Exception as e:
        raise e(f"Cannot extract a valid DOI from the provided URL: {url}")

