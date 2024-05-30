import pytest

from src.test.test3.wikilink_parser import *
from src.test.test3.wikilink_pathfinder import *


def test_get_all_links_from_node() -> None:
    links = get_all_links(get_page_from_url("https://en.wikipedia.org/wiki/Toilet_paper_orientation"))
    node = Node(None, "https://en.wikipedia.org/wiki/Toilet_paper_orientation")
    assert all(node.link in links for node in get_all_links_from_node(node, set()))


def test_get_path_from_node() -> None:
    node = Node(Node(Node(Node(None, "konec"), "3"), "2"), "1")
    assert get_path_from_node(node) == ["konec", "3", "2", "1"]


def test_find_shortest_link_between_2() -> None:
    path = find_shortest_link_path_between_2(
        "https://en.wikipedia.org/wiki/Nazi_Germany", "https://en.wikipedia.org/wiki/Adolf_Hitler", set(), 5
    )
    assert path == ["https://en.wikipedia.org/wiki/Nazi_Germany", "https://en.wikipedia.org/wiki/Adolf_Hitler"]
