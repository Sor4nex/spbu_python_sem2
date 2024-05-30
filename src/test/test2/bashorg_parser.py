import random

import requests
from bs4 import BeautifulSoup


def parse_response(response: requests.models.Response, elem_num: int) -> list[str]:
    parser = BeautifulSoup(response.text, "html.parser")
    quotes = parser.findAll("div", class_="quote__body")
    for br in parser.find_all("br"):
        br.replace_with("\n")
    return [elem.text for elem in quotes[:elem_num]]


async def get_latest_quotes(elem_number: int) -> list[str]:
    def find_page_number(response: requests.models.Response) -> int:
        parser = BeautifulSoup(response.text, "html.parser")
        snippets = parser.findAll("input", class_="pager__input")
        return int(snippets[0]["max"])

    result_quotes = []
    page_numm = find_page_number(requests.get("https://башорг.рф/"))
    while elem_number > 0:
        request_response = requests.get(f"https://башорг.рф/index/{str(page_numm)}")
        parsed_quotes = parse_response(request_response, elem_number)
        result_quotes += [elem.rstrip().lstrip() for elem in parsed_quotes]
        elem_number -= len(parsed_quotes)
        page_numm -= 1
    return result_quotes


async def get_best_quotes(elem_number: int) -> list[str]:
    result_quotes = []
    i = 1
    while elem_number > 0:
        request_response = requests.get(f"https://башорг.рф/byrating/{i}")
        parsed_quotes = parse_response(request_response, elem_number)
        result_quotes += [elem.rstrip().lstrip() for elem in parsed_quotes]
        i += 1
        elem_number -= len(result_quotes)
    return result_quotes


async def get_random_quotes(elem_number: int) -> list[str]:
    result_quotes = []
    while elem_number > 0:
        seed = str(random.randint(1, 9999)).rjust(4, "0")
        request_response = requests.get(f"https://башорг.рф/random?{seed}")
        parsed_quotes = parse_response(request_response, elem_number)
        result_quotes += [elem.rstrip().lstrip() for elem in parsed_quotes]
        elem_number -= len(parsed_quotes)
    return result_quotes
