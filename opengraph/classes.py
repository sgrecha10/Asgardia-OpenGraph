"""Additional classes module for app 'asgardia'

Classes:
ExtendedHtmlParser
OpenGraph
"""
from typing import List, Optional, Any
from html.parser import HTMLParser
import urllib.request
import json


class ExtendedHtmlParser(HTMLParser):
    """Class for parsing meta tags from html. This class is used by another class"""
    html: Optional[str]
    data: List[str]

    def __init__(self, html: Optional[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = []
        if html is not None:
            self.feed(html)

    def handle_starttag(self, tag: str, attrs: List[Any]) -> None:
        if tag == 'meta' \
                and any((_[1].startswith('og:') for _ in attrs if hasattr(_[1], 'startswith'))):
            self.data.append(str(self.get_starttag_text()))

    def get_data(self) -> List[str]:
        """This method returns a list of meta tags"""
        return self.data


class OpenGraph:
    """This end-class receives a URL.
    This class contains methods for returning Open Graph markup and error messages.
    """
    url: str
    data: List[str]
    messages: List[str]

    def __init__(self, url: Optional[str] = None) -> None:
        self.data = []
        self.messages = []
        if url is not None:
            self.url = url
            self._to_parse()

    def _get_url(self) -> Optional[str]:
        try:
            with urllib.request.urlopen(self.url) as raw:
                return raw.read().decode('utf-8')
        except Exception:
            self.messages.append('Ошибка URL или ошибка удаленного сервера')
            return None

    def _to_parse(self) -> None:
        parser = ExtendedHtmlParser(self._get_url())
        self.data = parser.get_data()
        if not self.data:
            self.messages.append('Разметка Open Graph отсутствует')

    def get_list(self) -> List[str]:
        """This method returns the original list of meta tags"""
        return self.data

    def get_json(self) -> str:
        """This method returns a list of meta tags in json"""
        return json.dumps(self.data)

    def get_messages(self) -> List[str]:
        """This method returns a list of error messages"""
        return self.messages
