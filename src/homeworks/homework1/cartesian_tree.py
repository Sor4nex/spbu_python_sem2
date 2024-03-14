from copy import deepcopy
from random import uniform
from typing import Generic, Iterator, MutableMapping, Optional, Protocol, TypeVar

STRING_CARTESIAN_TREE_ID = "Cartesian Tree, id: {}, elements count: {}."
STRING_FEATURES = "key|priority|value"
ERROR_EMPTY_TREE = "tree is empty"
ERROR_KEY_NOT_FOUND = "key {} not found"


class Comparable(Protocol):
    def __lt__(self, other: "NodeKey") -> bool:
        return self < other


NodeKey = TypeVar("NodeKey", bound=Comparable)
NodeValue = TypeVar("NodeValue")


class Node(Generic[NodeKey, NodeValue]):
    def __init__(self, key: NodeKey, value: NodeValue, priority_upper_bound: float = 1.0) -> None:
        self.key: NodeKey = key
        self.value: NodeValue = value
        self.priority: float = uniform(priority_upper_bound, 0)
        self.left_node: Optional["Node"] = None
        self.right_node: Optional["Node"] = None

    def __repr__(self) -> str:
        return f"{self.key}|{self.priority}|{self.value}"


class CartesianTree(MutableMapping, Generic[NodeKey, NodeValue]):
    tree_id = 0

    def __init__(self) -> None:
        self.root: Optional[Node[NodeKey, NodeValue]] = None
        self.id: int = CartesianTree.tree_id
        self.elements_count: int = 0
        CartesianTree.tree_id += 1

    def __getitem__(self, key: NodeKey) -> NodeValue:
        search_result: Optional[Node[NodeKey, NodeValue]] = CartesianTree._get_node_recursively(key, self.root)
        if search_result is None:
            raise KeyError(ERROR_KEY_NOT_FOUND.format(key))
        return search_result.value

    def __setitem__(self, key: NodeKey, value: NodeValue) -> None:
        def _add_recursively(
            key: NodeKey, node: Optional[Node[NodeKey, NodeValue]], priority_upper_bound: float
        ) -> Node[NodeKey, NodeValue]:
            if node is None:
                return Node(key, value, priority_upper_bound)
            elif key > node.key:
                node.right_node = _add_recursively(key, node.right_node, node.priority)
            elif key < node.key:
                node.left_node = _add_recursively(key, node.left_node, node.priority)
            else:
                node.value = value
            return node

        self.elements_count += 1 if CartesianTree._get_node_recursively(key, self.root) is None else 0
        if self.root is None:
            priority = 1.0
        else:
            priority = self.root.priority
        self.root = _add_recursively(key, self.root, priority)

    def __delitem__(self, key: NodeKey) -> None:
        def get_minimal_node(node: Node[NodeKey, NodeValue]) -> Node[NodeKey, NodeValue]:
            return get_minimal_node(node.left_node) if node.left_node is not None else node

        def _del_recursively(
            key: NodeKey, node: Optional[Node[NodeKey, NodeValue]]
        ) -> Optional[Node[NodeKey, NodeValue]]:
            if node is None:
                raise KeyError(ERROR_KEY_NOT_FOUND.format(key))
            elif key > node.key:
                node.right_node = _del_recursively(key, node.right_node)
                return node
            elif key < node.key:
                node.left_node = _del_recursively(key, node.left_node)
                return node
            if node.right_node is None and node.left_node is None:
                return None
            elif node.right_node is None or node.left_node is None:
                return node.right_node if node.left_node is None else node.left_node
            else:
                minimal_node = get_minimal_node(node)
                node = _del_recursively(minimal_node.key, node)
                if node is not None:
                    node.key = minimal_node.key
                    node.value = minimal_node.value
                    return node

        self.root = _del_recursively(key, self.root)
        self.elements_count -= 1

    def __iter__(self) -> Iterator[NodeKey]:
        def _traverse(node: Optional[Node[NodeKey, NodeValue]]) -> Iterator[NodeKey]:
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
        return self.elements_count

    def __eq__(self, other: object) -> bool:
        def _check_eq_recursively(
            node1: Optional[Node[NodeKey, NodeValue]], node2: Optional[Node[NodeKey, NodeValue]]
        ) -> bool:
            if node1 is None and node2 is None:
                return True
            elif node1 is None or node2 is None:
                return False
            elif (node1.key == node2.key) and (node1.value == node2.value):
                return _check_eq_recursively(node1.left_node, node2.left_node) and _check_eq_recursively(
                    node1.right_node, node2.right_node
                )
            return False

        if not isinstance(other, CartesianTree):
            return NotImplemented
        return _check_eq_recursively(self.root, other.root)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        if self.root is None:
            return STRING_CARTESIAN_TREE_ID.format(self.id, self.elements_count) + "\nempty\n"
        output_string = [STRING_CARTESIAN_TREE_ID.format(self.id, self.elements_count), STRING_FEATURES]
        for node_key in self:
            node = CartesianTree._get_node_recursively(node_key, self.root)
            if node is not None:
                output_string.append(f"{node_key};{round(node.priority, 3)};{node.value}")
        return "\n".join(output_string) + "\n"

    @staticmethod
    def _recount_tree_elem_count(Tree: "CartesianTree") -> int:
        def _recount_elem_recursively(node: Optional[Node[NodeKey, NodeValue]]) -> int:
            if node is None:
                return 0
            return 1 + _recount_elem_recursively(node.left_node) + _recount_elem_recursively(node.right_node)

        return _recount_elem_recursively(Tree.root)

    @staticmethod
    def _get_node_recursively(
        key: NodeKey, node: Optional[Node[NodeKey, NodeValue]]
    ) -> Optional[Node[NodeKey, NodeValue]]:
        if node is None:
            return None
        elif key > node.key:
            return CartesianTree._get_node_recursively(key, node.right_node)
        elif key < node.key:
            return CartesianTree._get_node_recursively(key, node.left_node)
        else:
            return node

    def split(self, key: NodeKey) -> tuple["CartesianTree", "CartesianTree"]:
        def _split_recursively(
            key: NodeKey, node: Optional[Node[NodeKey, NodeValue]]
        ) -> tuple[Optional[Node[NodeKey, NodeValue]], Optional[Node[NodeKey, NodeValue]]]:
            if node is None:
                return None, None
            if key > node.key:
                node1, node2 = _split_recursively(key, node.right_node)
                node.right_node = node1
                return node, node2
            else:
                node1, node2 = _split_recursively(key, node.left_node)
                node.left_node = node2
                return node1, node

        tree1: CartesianTree = CartesianTree()
        tree2: CartesianTree = CartesianTree()
        tree1.root, tree2.root = _split_recursively(key, deepcopy(self.root))
        tree1.elements_count = CartesianTree._recount_tree_elem_count(tree1)
        tree2.elements_count = CartesianTree._recount_tree_elem_count(tree2)
        return tree1, tree2

    def merge(self, other: "CartesianTree") -> "CartesianTree":
        def _merge_recursively(
            node1: Optional[Node[NodeKey, NodeValue]], node2: Optional[Node[NodeKey, NodeValue]]
        ) -> Optional[Node[NodeKey, NodeValue]]:
            if node2 is None:
                return node1
            elif node1 is None:
                return node2
            elif node1.priority > node2.priority:
                node1.right_node = _merge_recursively(node1.right_node, node2)
                return node1
            else:
                node2.left_node = _merge_recursively(node1, node2.left_node)
                return node2

        result: CartesianTree = CartesianTree()
        result.root = _merge_recursively(deepcopy(self.root), deepcopy(other.root))
        result.elements_count = CartesianTree._recount_tree_elem_count(result)
        return result
