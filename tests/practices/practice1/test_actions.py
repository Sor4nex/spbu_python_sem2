import hypothesis
import hypothesis.strategies as st
import pytest

from src.practices.practice1.actions import *


class TestActions:
    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250), st.integers(min_value=0, max_value=250), st.integers()
    )
    def test_action_insert_apply(self, initial_list, insert_pos, value) -> None:
        start_len = len(initial_list)

        hypothesis.assume(insert_pos < start_len)

        action = ActionInsert(insert_pos, value)
        action.apply(initial_list)

        assert start_len == len(initial_list) - 1
        assert initial_list[insert_pos] == value

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250), st.integers(min_value=0, max_value=250), st.integers()
    )
    def test_action_insert_undo(self, initial_list, insert_pos, value) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(insert_pos < start_len)

        action = ActionInsert(insert_pos, value)
        action.apply(initial_list)
        action.undo(initial_list)

        assert initial_list == start_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250),
        st.integers(min_value=0, max_value=250),
        st.integers(min_value=0, max_value=250),
    )
    def test_action_change_position_apply(self, initial_list, pos1, pos2) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len and pos2 < start_len)

        action = ActionChangePositions(pos1, pos2)
        action.apply(initial_list)

        assert len(initial_list) == start_len
        assert initial_list[pos1] == start_list[pos2]
        assert initial_list[pos2] == start_list[pos1]

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250),
        st.integers(min_value=0, max_value=250),
        st.integers(min_value=0, max_value=250),
    )
    def test_action_change_position_undo(self, initial_list, pos1, pos2) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len and pos2 < start_len)

        action = ActionChangePositions(pos1, pos2)
        action.apply(initial_list)
        action.undo(initial_list)

        assert initial_list == start_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250), st.integers(min_value=0, max_value=250), st.integers()
    )
    def test_action_addition_apply(self, initial_list, pos1, value) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len)

        action = ActionAddition(pos1, value)
        action.apply(initial_list)

        assert len(initial_list) == start_len
        assert initial_list[pos1] == start_list[pos1] + value

        initial_list[pos1] -= value
        assert initial_list == start_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250), st.integers(min_value=0, max_value=250), st.integers()
    )
    def test_action_addition_undo(self, initial_list, pos1, value) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len)

        action = ActionAddition(pos1, value)
        action.apply(initial_list)
        action.undo(initial_list)

        assert initial_list == start_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=0, max_size=250), st.integers())
    def test_action_addition_all_apply(self, initial_list, value) -> None:
        start_list = initial_list[:]
        start_len = len(initial_list)

        action = ActionAdditionAll(value)
        action.apply(initial_list)

        assert start_len == len(initial_list)

        for i in range(start_len):
            assert initial_list[i] == start_list[i] + value

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=0, max_size=250), st.integers())
    def test_action_addition_all_undo(self, initial_list, value) -> None:
        start_list = initial_list[:]
        start_len = len(initial_list)

        action = ActionAdditionAll(value)
        action.apply(initial_list)
        action.undo(initial_list)

        assert start_list == initial_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=0, max_size=250), st.integers(min_value=0, max_value=250))
    def test_action_remove_apply(self, initial_list, pos) -> None:
        start_len = len(initial_list)

        hypothesis.assume(pos < len(initial_list))

        start_list = initial_list[:]
        value_to_remove = initial_list[pos]

        action = ActionRemove(pos)
        action.apply(initial_list)

        assert len(initial_list) == start_len - 1
        assert action.args[1] == value_to_remove

        initial_list.insert(pos, value_to_remove)
        assert initial_list == start_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=0, max_size=250), st.integers(min_value=0, max_value=250))
    def test_action_remove_undo(self, initial_list, pos) -> None:
        start_list = initial_list[:]
        start_len = len(start_list)

        hypothesis.assume(pos < start_len)
        action = ActionRemove(pos)
        action.apply(initial_list)
        action.undo(initial_list)

        assert initial_list == start_list
