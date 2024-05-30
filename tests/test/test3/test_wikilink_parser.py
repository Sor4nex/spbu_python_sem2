import pytest

from src.test.test3.wikilink_parser import *


def test_get_all_links() -> None:
    wiki_links = get_all_links(get_page_from_url("https://en.wikipedia.org/wiki/Adolf_Hitler"))
    assert all(link.startswith("https://en.wikipedia.org/wiki/") for link in wiki_links)
