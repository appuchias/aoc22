#! /usr/bin/env python3

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True, order=True, eq=True)
class Point:
    x: int = 0
    y: int = 0

    def get_neighbors(self):
        """Returns a list of the neighboring 8 points."""
        return _get_neighbors(self)

    def get_adjacent(self):
        """Retuns the 4 directly adjacent points"""
        return _get_adjacent(self)


def to_point(p: str | List[int], sep=" ") -> Point:
    if isinstance(p, str):
        p = [int(i) for i in p.split(sep)]

    return Point(*p)


def _get_neighbors(p: Point) -> List[Point]:
    return [
        Point(p.x + x, p.y + y)
        for x in range(-1, 2)
        for y in range(1, -2, -1)
        if x != p.x or y != p.y
    ]


def _get_adjacent(p: Point) -> List[Point]:
    return [
        Point(p.x, p.y + 1),
        Point(p.x + 1, p.y),
        Point(p.x, p.y - 1),
        Point(p.x - 1, p.y),
    ]
