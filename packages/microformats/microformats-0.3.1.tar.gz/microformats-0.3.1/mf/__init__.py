"""Microformats utilities."""

import collections
import importlib.metadata

import requests

from . import util
from .parser import Parser

__all__ = ["parse"]


def parse(doc=None, url=None, html_parser="html5lib", img_with_alt=False):
    """
    Return a dictionary containing the mf2json of the given HTML `doc`.

    You may provide a document, a URL or both. When both are provided
    the URL is used as the document's base href.

    You may specify an alternate `html_parser` with one of "html", "xml",
    "html5", "lxml", "html5lib" or "html.parser".

    Args:
      doc (file or string or BeautifulSoup doc): file handle, text of content
        to parse, or BeautifulSoup document. If None, it will be fetched from
        given url
      url (string): url of the file to be processed. Optionally extracted from
        base-element of given doc
    """
    url = str(url)
    metadata = importlib.metadata.metadata("microformats")
    useragent = f"{metadata['Home-page']} - version {metadata['Version']}"
    if doc is None:
        headers = {"User-Agent": useragent}
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.SSLError:
            response = requests.get(url, headers=headers, verify=False)
        doc = response.text
        url = response.url
    mf2json = Parser(doc, url, html_parser, img_with_alt).to_dict()
    mf2json["debug"]["user-agent"] = useragent
    return mf2json
