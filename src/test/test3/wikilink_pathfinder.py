import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Optional

from src.test.test3.wikilink_parser import get_all_links, get_page_from_url


@dataclass(frozen=True)
class Node:
    previous: Optional["Node"]
    link: str


def get_all_links_from_node(node: Node, already_visited: set) -> set[Node]:
    response = get_page_from_url(node.link)
    if response is None:
        return set()
    all_links = get_all_links(response)
    res = set()
    for link in all_links:
        if link in already_visited:
            continue
        res.add(Node(node, link))
    return res


def get_path_from_node(node: Node) -> list[str]:
    if node.previous is None:
        return [node.link]
    return get_path_from_node(node.previous) + [node.link]


def find_shortest_link_path_between_2(
    start_url: str, target_url: str, already_visited: set, n_processes: int, depth: int = 3
) -> Optional[list[str]]:
    already_visited.add(start_url)
    if start_url == target_url:
        return [start_url]

    curr_level = {Node(None, start_url)}
    i = 1
    with ProcessPoolExecutor(max_workers=n_processes) as executor:
        while i <= depth:
            print(f"\tChecking links on level {i}...")
            new_links_nodes = [executor.submit(get_all_links_from_node, node, already_visited) for node in curr_level]
            next_level = set()
            for links_set in as_completed(new_links_nodes):
                for node_link in links_set.result():
                    if node_link.link in already_visited:
                        continue
                    already_visited.add(node_link.link)
                    if node_link.link == target_url:
                        print("\tlink found!")
                        for elem in new_links_nodes:
                            elem.cancel()
                        executor.shutdown()
                        return get_path_from_node(node_link)
                    next_level.add(node_link)
            print(f"\tlevel {i} not found...")
            curr_level = next_level
            i += 1
    return None


def find_shortest_link_path(links: list[str], n_processes: int = 5, unique: bool = False) -> None:
    print("\nStart searching path:")
    print(" -> ... -> ".join(links), "\n")

    path = []
    already_visited: set = set()
    for i in range(1, len(links)):
        print(f"{i}. Searching path between {links[i - 1]} and {links[i]}:")
        shortest_path = find_shortest_link_path_between_2(links[i - 1], links[i], already_visited.copy(), n_processes)
        if shortest_path is None:
            print(f"\tPath between {links[i - 1]} and {links[i]} NOT FOUND")
            print(f"No path for\n", " -> ... -> ".join(links))
            return
        print("\tPath:", " -> ".join(shortest_path))
        path.append(shortest_path[1:-1])
        if unique:
            already_visited = set.union(already_visited, set(shortest_path))
    print("\nWhole path found:")
    print(links[0], end=" -> ")
    for i in range(len(path)):
        print(" -> ".join(path[i]), "->", links[i + 1], end=" -> ")
    print("\n")


def set_up_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("links", type=str, nargs="*")
    parser.add_argument("--n_processes", type=int, default=5)
    parser.add_argument("--unique", action="store_true")
    return parser


def main() -> None:
    arg_parser = set_up_arg_parser()
    args = arg_parser.parse_args()
    find_shortest_link_path(**vars(args))


if __name__ == "__main__":
    main()
