import argparse as ap
import random
from time import perf_counter
from typing import Callable

import pandas as pd
import seaborn as sns
from merge_sort import merge_sort, merge_sort_multithread


def draw_chart(measures: pd.DataFrame, chart_filename: str, n_elem: int) -> None:
    plot = sns.lineplot(measures)
    plot.set(xlabel="Threads number", ylabel="Time(sec.)", title=f"Merge sort time comp.({n_elem} elements)")
    plot.figure.savefig(chart_filename)


def time_function(func: Callable, *, args: tuple, n_iterations: int = 3) -> float:
    timings = []
    for _ in range(n_iterations):
        start_time = perf_counter()
        func(*args)
        timings.append(perf_counter() - start_time)
    return sum(timings) / n_iterations


def count_time_merge_sort_single_thread(unsorted_list: list[int], n_jobs: list[int]) -> list[float]:
    timings = []
    for _ in n_jobs:
        timings.append(time_function(merge_sort, args=(unsorted_list,)))
    return timings


def count_time_merge_sort_multithread(
    unsorted_list: list[int], n_jobs: list[int], *, multiprocess: bool = False
) -> list[float]:
    timings = []
    for i in n_jobs:
        timings.append(time_function(merge_sort_multithread, args=(unsorted_list, i, multiprocess)))
    return timings


def arg_parser_setup() -> ap.ArgumentParser:
    parser = ap.ArgumentParser()
    parser.add_argument("-ll", "--list_len", type=int, default=1_000_000)
    parser.add_argument("-nt", "--n_threads", type=int, default=8)
    parser.add_argument("-op", "--output-path", type=str, default="merge_sort_comp.png")
    parser.add_argument("--multiprocess", action="store_true")
    return parser


def main(list_len: int, output_path: str, n_threads: list[int], multiprocess: bool = False) -> None:
    unsorted_list = [random.randint(-1000, 1000) for _ in range(list_len)]
    time_computation = {
        "single thread": count_time_merge_sort_single_thread(unsorted_list, n_threads),
        "multithread": count_time_merge_sort_multithread(unsorted_list, n_threads, multiprocess=multiprocess),
    }
    time_dataframe = pd.DataFrame(data=time_computation, index=n_threads)
    draw_chart(time_dataframe, output_path, list_len)


if __name__ == "__main__":
    arg_parser = arg_parser_setup()
    args = arg_parser.parse_args()
    args.n_threads = range(2, args.n_threads)
    main(**vars(args))
