import re

import requests
from bs4 import BeautifulSoup


def get_all_links(response: requests.models.Response) -> list[str]:
    parser = BeautifulSoup(response.text, "html.parser")
    all_tags = parser.body.find("div", class_="mw-page-container").findAll(
        "a", href=re.compile("^/wiki/"), class_=False
    )
    res_wiki_links = []
    for tag in all_tags:
        link = tag["href"]
        if ":" in link:
            continue
        res_wiki_links.append("https://en.wikipedia.org" + tag["href"])
    return res_wiki_links


def get_article_name(response: requests.models.Response) -> str:
    parser = BeautifulSoup(response.text, "html.parser")
    return parser.find("span", "mw-page-title-main").text
