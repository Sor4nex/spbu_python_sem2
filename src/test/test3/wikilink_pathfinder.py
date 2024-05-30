from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Optional

from wikilink_parser import get_page_from_url, get_all_links


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
    for link in all_links - already_visited:
        res.add(Node(node, link))
    return res


def get_path_from_node(node: Node) -> list[str]:
    if node.previous is None:
        return [node.link]
    return get_path_from_node(node.previous) + [node.link]


def find_shortest_link_path(start_url: str, target_url: str, n_processes: int, depth: int = 5) -> Optional[list[str]]:
    already_visited = set()
    path_start = Node(None, start_url)
    curr_level = get_all_links_from_node(path_start, already_visited)
    i = 1
    with ProcessPoolExecutor(max_workers=n_processes) as executor:
        shortest_path: Optional[Node] = None
        while i <= depth:
            print("searchin lvl", i)
            new_links_nodes = [executor.submit(get_all_links_from_node, node, already_visited) for node in curr_level]
            next_level = set()
            for links in as_completed(new_links_nodes):
                next_level = set.union(next_level, links.result())
            print("next level got")
            repeated_links = []
            for node in next_level:
                if node.link == target_url:
                    shortest_path = node
                    break
                if node.link in already_visited:
                    repeated_links.append(node)
                already_visited.add(node.link)
            else:
                for node in repeated_links:
                    next_level.remove(node)
                print("repeated removed")
                curr_level = next_level
                i += 1
                continue
            break
        if shortest_path is not None:
            return get_path_from_node(shortest_path)
        return None


def main() -> None:
    print(find_shortest_link_path("https://en.wikipedia.org/wiki/Tmesipteris_horomaka", "https://en.wikipedia.org/wiki/Adolf_Hitler", 6))


if __name__ == "__main__":
    main()
