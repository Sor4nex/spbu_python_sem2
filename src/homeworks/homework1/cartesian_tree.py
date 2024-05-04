import random as rnd
from typing import Any, Generic, Iterator, MutableMapping, Optional, TypeVar

K = TypeVar("K")


class Node(Generic[K]):
    def __init__(self, key: K, value: Any) -> None:
        self.key = key
        self.value = value
        self.priority = rnd.random()
        self.right_node: Optional[Node[K]] = None
        self.left_node: Optional[Node[K]] = None

    def __str__(self) -> str:
        return f"[key:{self.key}|value:{self.value}|left key:{str(self.left_node)}|right key:{str(self.right_node)}]"

    def __repr__(self) -> str:
        return f"[key:{self.key}|value:{self.value}|priority:{self.priority:0.4f}|left key:{repr(self.left_node)}|right key:{repr(self.right_node)}]"


class CartesianTree(Generic[K], MutableMapping):
    def __init__(self) -> None:
        self.root: Optional[Node[K]] = None
        self.len: int = 0

    def __setitem__(self, key: K, value: Any) -> None:
        if key in self:
            del self[key]
        insert_element = Node(key, value)
        tree_left_key_split_root, tree_right_key_split_root = CartesianTree.split(key, self.root)
        tree_left_key_split_root = CartesianTree.merge(tree_left_key_split_root, insert_element)
        self.root = CartesianTree.merge(tree_left_key_split_root, tree_right_key_split_root)
        self.len += 1

    def __delitem__(self, key: K) -> None:
        def _del_recursively(key: Any, node: Optional[Node[K]]) -> Optional[Node[K]]:
            if node is None:
                raise KeyError(f"cannot delete node. Key {key} not found")
            elif key > node.key:
                node.right_node = _del_recursively(key, node.right_node)
            elif key < node.key:
                node.left_node = _del_recursively(key, node.left_node)
            else:
                return CartesianTree.merge(node.left_node, node.right_node)
            return node

        self.root = _del_recursively(key, self.root)
        self.len -= 1

    def __getitem__(self, key: K) -> Any:
        result = self._search_node(key, self.root)
        if result is None:
            raise KeyError(f"key {key} not found")
        return result.value

    def __iter__(self) -> Iterator[K]:
        def _traverse(node: Optional[Node[K]]) -> Iterator[K]:
            if node:
                yield from _traverse(node.left_node)
                yield node.key
                yield from _traverse(node.right_node)

        return _traverse(self.root)

    def __len__(self) -> int:
        return self.len

    def __repr__(self) -> str:
        if self.root:
            return f"[len:{self.len}]|root:{repr(self.root)}]"
        return "empty tree"

    def __str__(self) -> str:
        if self.root:
            return f"[len:{self.len}|root:{str(self.root)}]"
        return "empty tree"

    def _search_node(self, key: Any, node: Optional[Node[K]]) -> Optional[Node[K]]:
        if node is None:
            return None
        elif key > node.key:
            return self._search_node(key, node.right_node)
        elif key < node.key:
            return self._search_node(key, node.left_node)
        else:
            return node

    @staticmethod
    def split(key: Any, node: Optional[Node[K]]) -> tuple[Optional[Node[K]], Optional[Node[K]]]:
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
    def merge(node1: Optional[Node[K]], node2: Optional[Node[K]]) -> Optional[Node[K]]:
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
