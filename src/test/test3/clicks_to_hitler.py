import argparse
from collections import deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Optional

import requests
import wiki_links_parser as wlp


@dataclass
class LinkPath:
    depth: int
    path: list[str]


def find_shortest_link_path(links: list, max_depth: int, n_proccess: int) -> Optional[LinkPath]:
    link_queue: deque = deque()
    print(f"Process №{n_proccess} started!")
    for link in links:
        link_queue.append(LinkPath(1, [link]))
    while link_queue:
        curr_link = link_queue.popleft()
        if curr_link.depth > max_depth - 1:
            continue
        try:
            response = requests.get(curr_link.path[-1])
        except Exception:
            continue
        all_child_links = wlp.get_all_links(response)
        for link in all_child_links:
            new_link = LinkPath(curr_link.depth + 1, curr_link.path + [link])
            if "Adolf_Hitler" in link:
                print(f"Process №{n_proccess} found path (depth={curr_link.depth + 1})", " -> ".join(new_link.path))
                return new_link
            link_queue.append(new_link)
    print(f"Process №{n_proccess} found nothing")


def set_up_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("max_depth", type=int)
    parser.add_argument("n_processes", type=int)
    parser.add_argument("--url", type=str, default="https://en.wikipedia.org/wiki/Special:Random")
    return parser


def main(url: str, n_processes: int, max_depth: int) -> None:
    try:
        response = requests.get(url)
    except Exception as e:
        print("unexpected error while trying to request url:", e)
        return
    if "Random" in url:
        article_name = wlp.get_article_name(response)
        url = f"https://en.wikipedia.org/wiki/{article_name}"
    starting_links = wlp.get_all_links(response)
    for link in starting_links:
        if "Adolf_Hitler" in link:
            print(f"Minimal path (depth = 1):\n{url} -> {link}")
            return
    n_links = len(starting_links)
    slice_len = n_links // n_processes
    starting_links_slices = [starting_links[i : i + slice_len] for i in range(0, n_links, slice_len)]
    with ProcessPoolExecutor(max_workers=n_processes) as executor:
        shortest_paths = [
            executor.submit(find_shortest_link_path, link_slice, max_depth, i + 1)
            for i, link_slice in enumerate(starting_links_slices)
        ]
        paths: list[LinkPath] = []
        for path in as_completed(shortest_paths):
            res = path.result()
            if res is None:
                continue
            paths.append(res)
    if paths:
        minimal = min(paths, key=lambda x: x.depth)
        print(f"\nMinimal path (depth = {minimal.depth}):\n{url} -> {' -> '.join(minimal.path)}")
    else:
        print(f"No existing path with depth {max_depth}")


if __name__ == "__main__":
    parser = set_up_arg_parser()
    args = parser.parse_args()
    main(**vars(args))
