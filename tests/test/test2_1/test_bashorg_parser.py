import asyncio

import pytest

from src.test.test2.bashorg_parser import *


def test_get_best_quotes() -> None:
    result = asyncio.run(get_best_quotes(7))
    assert len(result) == 7
    assert isinstance(result[0], str)


def test_get_latest_quotes() -> None:
    result = asyncio.run(get_latest_quotes(7))
    assert len(result) == 7
    assert isinstance(result[0], str)


def test_get_random_quotes() -> None:
    result = asyncio.run(get_random_quotes(7))
    assert len(result) == 7
    assert isinstance(result[0], str)
