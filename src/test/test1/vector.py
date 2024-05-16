from typing import Any, Generic, Protocol, TypeVar


class DimensionalError(Exception):
    def __init__(self, text: str) -> None:
        self.txt = text


class ArithmeticAvailable(Protocol):
    def __add__(self, other: Any) -> Any:
        raise NotImplementedError

    def __sub__(self, other: Any) -> Any:
        raise NotImplementedError

    def __mul__(self, other: Any) -> Any:
        raise NotImplementedError


T = TypeVar("T", bound=ArithmeticAvailable)


class Vector(Generic[T]):
    def __init__(self, given_coords: list[T]) -> None:
        self.coords: list[T] = given_coords
        self.dim: int = len(given_coords)

    def __add__(self, other: "Vector") -> "Vector":
        if self.dim != other.dim:
            raise DimensionalError("unequal dimensions")
        return Vector([self.coords[i] + other.coords[i] for i in range(self.dim)])

    def __sub__(self, other: "Vector") -> "Vector":
        if self.dim != other.dim:
            raise DimensionalError("unequal dimensions")
        return Vector([self.coords[i] - other.coords[i] for i in range(self.dim)])

    def __str__(self) -> str:
        return "(" + ";".join([str(elem) for elem in self.coords]) + ")"

    def __len__(self) -> int:
        return self.dim

    def scalar_multiply(self, other: "Vector") -> float:
        if self.dim != other.dim:
            raise DimensionalError("unequal dimensions")
        return sum([self.coords[i] * other.coords[i] for i in range(self.dim)])

    def vector_multiply(self, other: "Vector") -> "Vector":
        if self.dim != 3 or other.dim != 3:
            raise DimensionalError("both vectors should be 3-dimensional")
        x1, y1, z1 = self.coords
        x2, y2, z2 = other.coords
        res1 = y1 * z2 - z1 * y2
        res2 = z1 * x2 - x1 * z2
        res3 = x1 * y2 - y1 * x2
        return Vector([res1, res2, res3])

    def is_null(self) -> bool:
        return not any(self.coords)

    def get_len(self) -> float:
        return sum(map(lambda x: x * x, self.coords)) ** 0.5
