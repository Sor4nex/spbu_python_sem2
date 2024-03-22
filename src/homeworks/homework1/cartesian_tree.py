import random as rnd
from typing import Any, Generic, Iterator, MutableMapping, Optional, Protocol, TypeVar

STRING_TREE_REPR = "(id:{},len:{},root:{},{})"
STRING_TREE_STR = """tree id: {},
element number: {},
root: {},
all nodes:
key|value|priority|left|right"""


class Comparable(Protocol):
    def __lt__(self, other: "NodeKey") -> bool:
        return self < other


NodeKey = TypeVar("NodeKey", bound=Comparable)


class Node(Generic[NodeKey]):
    def __init__(self, key: NodeKey, value: Any) -> None:
        self.key = key
        self.value = value
        self.priority = rnd.random()
        self.right_node: Optional[Node[NodeKey]] = None
        self.left_node: Optional[Node[NodeKey]] = None

    def __str__(self) -> str:
        node_data = self.get_node_data()
        return f"key:{node_data[0]}|value{node_data[2]}|priority:{node_data[1]}|left key:{node_data[3]}|right key:{node_data[4]}"

    def get_node_data(self) -> tuple:
        right = (self.right_node.key, self.right_node.value) if self.right_node is not None else None
        left = (self.left_node.key, self.left_node.value) if self.left_node is not None else None
        return self.key, self.priority, self.value, left, right


class CartesianTree(Generic[NodeKey], MutableMapping):
    tree_id = 0

    def __init__(self) -> None:
        self.root: Optional[Node[NodeKey]] = None
        self.len: int = 0
        self.id = CartesianTree.tree_id
        CartesianTree.tree_id += 1

    def __setitem__(self, key: NodeKey, value: Any) -> None:
        if key in self:
            del self[key]
        insert_element = Node(key, value)
        tree_left_key_split_root, tree_right_key_split_root = CartesianTree.split(key, self.root)
        tree_left_key_split_root = CartesianTree.merge(tree_left_key_split_root, insert_element)
        self.root = CartesianTree.merge(tree_left_key_split_root, tree_right_key_split_root)
        self.len += 1

    def __delitem__(self, key: NodeKey) -> None:
        def _del_recursively(key: NodeKey, node: Optional[Node[NodeKey]]) -> Optional[Node[NodeKey]]:
            if node is None:
                raise KeyError()
            elif key > node.key:
                node.right_node = _del_recursively(key, node.right_node)
                return node
            elif key < node.key:
                node.left_node = _del_recursively(key, node.left_node)
                return node
            return CartesianTree.merge(node.left_node, node.right_node)

        self.root = _del_recursively(key, self.root)
        self.len -= 1

    def __getitem__(self, key: NodeKey) -> Any:
        result = CartesianTree._search_node(key, self.root)
        if result is None:
            raise KeyError(f"key {key} not found")
        return result.value

    def __iter__(self) -> Iterator[NodeKey]:
        def _traverse(node: Optional[Node[NodeKey]]) -> Iterator[NodeKey]:
            if node is None:
                pass
            elif node.right_node is None and node.left_node is None:
                yield node.key
            else:
                if node.left_node is not None:
                    yield from _traverse(node.left_node)
                yield node.key
                if node.right_node is not None:
                    yield from _traverse(node.right_node)

        return _traverse(self.root)

    def __len__(self) -> int:
        return self.len

    def __repr__(self) -> str:
        tree_data = self._get_tree_data()
        return STRING_TREE_REPR.format(
            tree_data["tree_id"], tree_data["tree_len"], tree_data["root"], tree_data["nodes"]
        )

    def __str__(self) -> str:
        tree_data = self._get_tree_data()
        output_str = STRING_TREE_STR.format(tree_data["tree_id"], tree_data["tree_len"], tree_data["root"])
        for node in tree_data["nodes"]:
            output_str += "\n" + f"{node[0]}|{node[2]}|{node[1]}|[{node[3]},{node[4]}]"
        return output_str

    @staticmethod
    def _search_node(key: NodeKey, node: Optional[Node[NodeKey]]) -> Optional[Node[NodeKey]]:
        if node is None:
            return None
        elif key > node.key:
            return CartesianTree._search_node(key, node.right_node)
        elif key < node.key:
            return CartesianTree._search_node(key, node.left_node)
        else:
            return node

    def _get_tree_data(self) -> dict:
        tree_data: dict = {
            "tree_id": self.tree_id,
            "tree_len": len(self),
            "root": (self.root.key, self.root.value) if self.root is not None else None,
            "nodes": [],
        }
        for key in self:
            node = CartesianTree._search_node(key, self.root)
            if node is not None:
                tree_data["nodes"].append(node.get_node_data())
        return tree_data

    @staticmethod
    def split(key: NodeKey, node: Optional[Node[NodeKey]]) -> tuple[Optional[Node[NodeKey]], Optional[Node[NodeKey]]]:
        if node is None:
            return None, None
        if key > node.key:
            node1, node2 = CartesianTree.split(key, node.right_node)
            node.right_node = node1
            return node, node2
        else:
            node1, node2 = CartesianTree.split(key, node.left_node)
            node.left_node = node2
            return node1, node

    @staticmethod
    def merge(node1: Optional[Node[NodeKey]], node2: Optional[Node[NodeKey]]) -> Optional[Node[NodeKey]]:
        if node2 is None:
            return node1
        elif node1 is None:
            return node2
        elif node1.priority > node2.priority:
            node1.right_node = CartesianTree.merge(node1.right_node, node2)
            return node1
        else:
            node2.left_node = CartesianTree.merge(node1, node2.left_node)
            return node2
