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


def merge_sort_multithread(unsorted_list: list[int], n_jobs: int, multiprocess: bool = False) -> list[int]:
    pool = ThreadPoolExecutor if not multiprocess else ProcessPoolExecutor
    slice_len = len(unsorted_list) // n_jobs
    list_slices = [unsorted_list[j : j + slice_len] for j in range(0, len(unsorted_list), slice_len)]
    res: list[int] = []
    with pool(max_workers=n_jobs) as executor:
        sorted_parts = [executor.submit(merge_sort, single_slice) for single_slice in list_slices]
        for part in as_completed(sorted_parts):
            res = unite_sorted_sublists(res, part.result())
    return res
