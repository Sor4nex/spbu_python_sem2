import copy
import random

import pytest

from src.homeworks.homework1.cartesian_tree import *


def check_tree_correctness(tree: CartesianTree) -> bool:
    def _check_correctness_recursively(node: Node) -> bool:
        if node is None:
            return True
        current_node_correctness = True
        if node.left_node is not None:
            current_node_correctness = (
                (node.left_node.key < node.key)
                and (node.left_node.priority < node.priority)
                and current_node_correctness
            )
        if node.right_node is not None:
            current_node_correctness = (
                (node.right_node.key > node.key)
                and (node.right_node.priority < node.priority)
                and current_node_correctness
            )
        return (
            _check_correctness_recursively(node.left_node)
            and current_node_correctness
            and _check_correctness_recursively(node.right_node)
        )

    return _check_correctness_recursively(tree.root)


def test_tree_set_item() -> None:
    results = []
    for _ in range(100):
        nodes_count = random.randint(1, 100)
        test_tree_object = CartesianTree()
        for _ in range(nodes_count):
            test_tree_object[random.randint(1, 1000)] = random.randint(1, 100)
        results.append(check_tree_correctness(test_tree_object))
    assert all(results)


def test_tree_set_item_elem_counts() -> None:
    test_tree_object = CartesianTree()
    for i in range(1, 101):
        test_tree_object[i] = i
        test_tree_object[-i] = -i
    assert test_tree_object.len == 200

    test_tree_object[35] = 6
    assert test_tree_object.len == 200


test_tree_1 = CartesianTree()
test_tree_1["ya prikupil ogromni bike"] = 52


def test_tree_get_item_exception_case() -> None:
    with pytest.raises(KeyError):
        test_tree_1["etogo netu v mudrom dreve"]


def test_tree_contains() -> None:
    result_key_present = "ya prikupil ogromni bike" in test_tree_1
    result_key_not_present = "rubi ih dahao" not in test_tree_1
    result_empty_tree = "chevoooo" not in CartesianTree()
    assert result_key_present and result_key_not_present and result_empty_tree


def test_tree_delitem() -> None:
    results = []
    for _ in range(100):
        nodes_count = random.randint(3, 100)
        random_node_key = random.randint(1, nodes_count - 1)
        test_tree_object = CartesianTree()
        for key in range(nodes_count):
            test_tree_object[key] = random.randint(0, 100)
        tree_elem_count = test_tree_object.len
        del test_tree_object[random_node_key]
        results.append(
            (check_tree_correctness(test_tree_object))
            and random_node_key not in test_tree_object
            and (test_tree_object.len == tree_elem_count - 1)
        )
    assert all(results)


def test_tree_delitem_exception_case() -> None:
    with pytest.raises(KeyError):
        del test_tree_1["ABUTALABASHUNEBA"]  # Dela idut ATLICHNA!


def test_tree_delitem_exception_case_empty_tree() -> None:
    with pytest.raises(KeyError):
        del CartesianTree()["WITCH DOCTAR, SЫN SH..."]


def test_tree_iter() -> None:
    test_tree = CartesianTree()
    all_keys = list(range(0, 101))
    random.shuffle(all_keys)
    for key in all_keys:
        test_tree[key] = random.randint(1, 100)
    for key in test_tree:
        all_keys.remove(key)
    assert all_keys == []


def test_tree_iter_empty_tree() -> None:
    test_tree = CartesianTree()
    assert list(test_tree.__iter__()) == []


def test_tree_len() -> None:
    results = []
    for i in range(40, 50):
        test_tree_object = CartesianTree()
        for j in range(i):
            test_tree_object[j] = j
        results.append(len(test_tree_object) == i)
    assert all(results)


def test_tree_eq() -> None:
    results = []

    test_tree1 = CartesianTree()
    test_tree2 = CartesianTree()
    results.append(test_tree1 == test_tree2)

    test_tree1[1] = 1
    results.append(not (test_tree1 == test_tree2))

    test_tree2[1] = 1
    test_tree2[2] = 2
    test_tree1[2] = 2
    results.append(test_tree1 == test_tree2)

    del test_tree2[2]
    results.append(not (test_tree1 == test_tree2))

    test_tree2[2] = 1
    results.append(not (test_tree1 == test_tree2))

    assert all(results)


def test_tree_keys() -> None:
    test_tree = CartesianTree()
    all_keys = list(range(0, 101))
    random.shuffle(all_keys)
    for key in all_keys:
        test_tree[key] = random.randint(1, 100)
    assert sorted(all_keys) == list(test_tree.keys())


def test_tree_keys_empty_tree() -> None:
    test_tree = CartesianTree()
    assert list(test_tree.keys()) == []


def test_tree_items() -> None:
    for _ in range(100):
        test_tree_object = CartesianTree()
        expected_items = []
        tree_keys = list(range(2, random.randint(3, 100)))
        random.shuffle(tree_keys)
        for key in tree_keys:
            value = random.randint(1, 1000)
            expected_items.append((key, value))
            test_tree_object[key] = value
        assert list(test_tree_object.items()) == sorted(expected_items, key=lambda x: x[0])


def test_tree_items_empty_tree() -> None:
    test_tree = CartesianTree()
    assert list(test_tree.items()) == []


def test_split() -> None:
    for _ in range(1000):
        start_tree = CartesianTree()
        for _ in range(random.randint(3, 100)):
            start_tree[random.randint(1, 1000)] = random.randint(1, 1000)
        split_value = random.randint(-10, 1010)
        start_tree_copy = copy.deepcopy(start_tree)
        tree_split1, tree_split2 = CartesianTree(), CartesianTree()
        tree_split1.root, tree_split2.root = CartesianTree.split(split_value, start_tree.root)
        tree1_keys_less_split_value = all(key < split_value for key in tree_split1)
        tree2_keys_greater_split_value = all(key >= split_value for key in tree_split2)
        assert (
            check_tree_correctness(tree_split1)
            and check_tree_correctness(tree_split2)
            and tree1_keys_less_split_value
            and tree2_keys_greater_split_value
            and list(tree_split1.items()) + list(tree_split2.items()) == list(start_tree_copy.items())
        )


def test_merge() -> None:
    for _ in range(1000):
        start_tree1, start_tree2 = CartesianTree(), CartesianTree()
        elem_number = random.randint(3, 100)
        random_key_border = random.randint(0, 1001)
        for i in range(elem_number):
            key = random.randint(1, 1000)
            if key < random_key_border:
                start_tree1[key] = random.randint(1, 1000)
            elif key > random_key_border:
                start_tree2[key] = random.randint(1, 1000)
        start_tree1_copy, start_tree2_copy = copy.deepcopy(start_tree1), copy.deepcopy(start_tree2)
        tree_merged = CartesianTree()
        tree_merged.root = CartesianTree.merge(start_tree1.root, start_tree2.root)
        assert check_tree_correctness(tree_merged) and list(start_tree1_copy.items()) + list(
            start_tree2_copy.items()
        ) == list(tree_merged.items())
