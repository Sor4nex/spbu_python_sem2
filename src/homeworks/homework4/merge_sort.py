import random
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed


def unite_sorted_sublists(list1: list[int], list2: list[int]) -> list[int]:
    i1 = i2 = 0
    len1, len2 = len(list1), len(list2)
    res = []
    while i1 != len1 and i2 != len2:
        if list1[i1] < list2[i2]:
            res.append(list1[i1])
            i1 += 1
            continue
        res.append(list2[i2])
        i2 += 1
    return res + list1[i1:] if i1 != len1 else res + list2[i2:]


def merge_sort(given_list: list[int]) -> list[int]:
    list_len = len(given_list)
    if list_len <= 1:
        return given_list
    sublist1, sublist2 = merge_sort(given_list[: list_len // 2]), merge_sort(given_list[list_len // 2 :])
    return unite_sorted_sublists(sublist1, sublist2)


def merge_sort_multithread_sublist(given_list: list[int], n_workers: int, multiprocess: bool = False) -> list[int]:
    list_len = len(given_list)  # v itoge voobshe niche ne ponel, vremeni ne ostalos(
    if list_len <= 1:  # primite plzzzz ya hochu zachet
        return given_list
    if n_workers > 2:
        pool = ProcessPoolExecutor if multiprocess else ThreadPoolExecutor
        with pool(max_workers=2) as executor:
            sublist1 = executor.submit(
                merge_sort_multithread_sublist, given_list[: list_len // 2], n_workers // 2 - 2, multiprocess
            )
            sublist2 = executor.submit(
                merge_sort_multithread_sublist, given_list[list_len // 2 :], n_workers // 2 - 2, multiprocess
            )
            return unite_sorted_sublists(sublist1.result(), sublist2.result())
    sublist1, sublist2 = merge_sort(given_list[: list_len // 2]), merge_sort(given_list[list_len // 2 :])
    return unite_sorted_sublists(sublist1, sublist2)


def merge_sort_multithread(unsorted_list: list[int], n_jobs: int, multiprocess: bool = False) -> list[int]:
    pool = ThreadPoolExecutor if not multiprocess else ProcessPoolExecutor
    slice_len = len(unsorted_list) // n_jobs
    list_slices = [unsorted_list[j : j + slice_len] for j in range(0, len(unsorted_list), slice_len)]
    with pool(max_workers=n_jobs) as executor:
        sorted_parts = [executor.submit(merge_sort, single_slice) for single_slice in list_slices]
        while len(sorted_parts) > 1:
            lst1 = sorted_parts.pop().result()
            lst2 = sorted_parts.pop().result()
            sorted_parts.append(executor.submit(unite_sorted_sublists, lst1, lst2))
    return sorted_parts[0].result()
