import re
from typing import Optional

import requests
from bs4 import BeautifulSoup


def get_page_from_url(url: str) -> Optional[requests.models.Response]:
    try:
        response = requests.get(url)
        return response
    except Exception as e:
        print("something went wrong:", e)


def get_all_links(response: requests.models.Response) -> set[str]:
    parser = BeautifulSoup(response.text, "html.parser")
    all_tags = parser.body.find("div", class_="mw-page-container").findAll(
        "a", href=re.compile("^/wiki/"), class_=False
    )
    res_wiki_links = set()
    for tag in all_tags:
        link = tag["href"]
        if ":" in link:
            continue
        res_wiki_links.add("https://en.wikipedia.org" + tag["href"])
    return res_wiki_links
