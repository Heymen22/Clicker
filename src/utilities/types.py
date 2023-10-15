from typing import NamedTuple, Sequence


class Point(NamedTuple):
    x: int
    y: int


class MacrosType(NamedTuple):
    id: int
    name: str
    points: Sequence[Point]
