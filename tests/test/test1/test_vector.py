import pytest

from src.test.test1.vector import *


def test_vector_init() -> None:
    vector = Vector([1, 2, 3, 4])
    assert len(vector.coords) == 4
    assert vector.dim == 4
    assert vector.coords == [1, 2, 3, 4]


def test_vector_addition() -> None:
    vect1, vect2 = Vector([1, 2, 3, 4]), Vector([5, 6, 7, 8])
    result = vect1 + vect2
    assert vect1.coords == [1, 2, 3, 4] and vect2.coords == [5, 6, 7, 8]
    assert isinstance(result, Vector)
    assert result.coords == [6, 8, 10, 12]


def test_vector_addition_exception() -> None:
    vect1, vect2 = Vector([1, 2, 3]), Vector([1, 2, 3, 4])
    with pytest.raises(DimensionalError):
        vect1 + vect2


def test_vector_subtraction() -> None:
    vect1, vect2 = Vector([1, 2, 3, 4]), Vector([5, 6, 7, 8])
    result = vect1 - vect2
    assert vect1.coords == [1, 2, 3, 4] and vect2.coords == [5, 6, 7, 8]
    assert isinstance(result, Vector)
    assert result.coords == [-4, -4, -4, -4]


def test_vector_subtraction_exception() -> None:
    vect1, vect2 = Vector([1, 2, 3]), Vector([1, 2, 3, 4])
    with pytest.raises(DimensionalError):
        vect1 - vect2


def test_vector_str() -> None:
    vect1 = Vector([1, 55, 324, 4])
    assert str(vect1) == "(1;55;324;4)"


def test_len() -> None:
    vect1 = Vector([1, 2, 3, 4, 5, 6, 7])
    assert len(vect1) == 7


def test_scalar_multiply() -> None:
    vect1, vect2 = Vector([1, 2, 3, 4]), Vector([5, 6, 7, 8])
    assert vect1.scalar_multiply(vect2) == 70


def test_scalar_multiply_exception() -> None:
    vect1, vect2 = Vector([1, 2, 3]), Vector([1, 2, 3, 4])
    with pytest.raises(DimensionalError):
        vect1.scalar_multiply(vect2)


def test_vector_multiply() -> None:
    vect1, vect2 = Vector([1, 2, 3]), Vector([5, 6, 7])
    result = vect1.vector_multiply(vect2)
    assert result.coords == [-4, 8, -4]


def test_vector_multiply_exception() -> None:
    vect1, vect2 = Vector([1, 2, 3]), Vector([1, 2, 3, 4])
    with pytest.raises(DimensionalError):
        vect1.vector_multiply(vect2)


def test_vector_is_null() -> None:
    vect_null = Vector([0, 0, 0])
    vect_not_null = Vector([1, 2])
    assert vect_null.is_null()
    assert not vect_not_null.is_null()


def test_get_len() -> None:
    vect1 = Vector([3, 4])
    assert vect1.get_len() == 5
