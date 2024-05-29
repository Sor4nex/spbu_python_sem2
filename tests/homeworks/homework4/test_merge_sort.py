from random import randint

import pytest

from src.homeworks.homework4.merge_sort import *


def test_unite_sorted_sublists() -> None:
    for _ in range(10):
        lst1 = sorted([randint(-100, 100) for _ in range(randint(2, 100))])
        lst2 = sorted([randint(-100, 100) for _ in range(randint(2, 100))])
        assert unite_sorted_sublists(lst1, lst2) == sorted(lst1 + lst2)


def test_merge_sort() -> None:
    for _ in range(50):
        lst = [randint(-1000, 1000) for _ in range(randint(2, 10000))]
        assert merge_sort(lst) == sorted(lst)


def test_merge_sort_multithread_v2() -> None:
    for _ in range(50):
        lst = [randint(-1000, 1000) for _ in range(randint(2, 10000))]
        assert merge_sort_multithread_sublist(lst, 10) == sorted(lst)

    for _ in range(50):
        lst = [randint(-1000, 1000) for _ in range(randint(2, 10000))]
        assert merge_sort_multithread_sublist(lst, 10, multiprocess=True) == sorted(lst)


def test_merge_sort_multithread() -> None:
    for _ in range(50):
        lst = [randint(-1000, 1000) for _ in range(randint(2, 10000))]
        assert merge_sort_multithread(lst, randint(1, 10)) == sorted(lst)

    for _ in range(50):
        lst = [randint(-1000, 1000) for _ in range(randint(2, 10000))]
        assert merge_sort_multithread(lst, randint(1, 10), multiprocess=True) == sorted(lst)
