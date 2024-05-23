import pytest

from src.test.test3.wiki_links_parser import *


@pytest.mark.parametrize("url", ["https://en.wikipedia.org/wiki/Special:Random"])
def test_get_article_name(url) -> None:
    res = get_article_name(requests.get(url))
    assert isinstance(res, str)
