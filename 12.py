#! /usr/bin/env python3

# Advent of Code 22 - Day 12

from typing import List
from models import Point
from dataclasses import dataclass, field


@dataclass()
class Path:
    start: Point
    end: Point
    path: List[Point] = field(default_factory=list)

    def append(self, p: Point) -> List[Point]:
        self.path.append(p)

        return self.path


def load_heightmap(fp: str) -> List[str]:
    with open(fp, "r") as f:
        content = [line.strip() for line in f.readlines()]

    return content


def find_char(heightmap: List[str], char: str) -> Point:
    p1 = heightmap.index([line for line in heightmap if char in line][0])
    return Point(heightmap[p1].index(char), p1)


def point_in_hm(heightmap: List[str], p: Point) -> bool:
    boundaries = [
        p.x < 0,
        p.y < 0,
        p.x > len(heightmap[0]) - 1,
        p.y > len(heightmap) - 1,
    ]
    return not any(boundaries)


def highest_adjacents(
    hm: List[str], path: List[Point], current_char: str, adjacent_p: List[Point]
) -> List[Point]:

    adjacent_p = list(
        filter(None, [p for p in adjacent_p if point_in_hm(hm, p) and p not in path])
    )

    adjacent_c: List[str] = [hm[p.y][p.x].replace("E", "z") for p in adjacent_p]

    # Remove points without 0<=Δ<=1 or outside board
    filter_fn = lambda t: (0 <= (ord(adjacent_c[t[0]]) - ord(current_char)) <= 1)
    adjacent = list(filter(filter_fn, enumerate(adjacent_p)))
    # Sort by greatest Δ
    adjacent = sorted(adjacent, reverse=True, key=lambda t: ord(hm[t[1].y][t[1].x]))

    return [i[1] for i in adjacent]


def pathfind(hm: List[str], start: Point, end: Point) -> ...:
    """Find all paths to go from `start` to `end` following the heightmap (`hm`)."""

    finished = False
    path: Path = Path(start, end, [Point(-1, -1)])

    current = start

    while not finished:
        current_char = hm[current.y][current.x].replace("S", "a")

        adjacent_p: List[Point] = current.get_adjacent()

        for p in adjacent_p:
            if p == end and (ord("z") - ord(current_char) <= 1):
                finished = True
                path.path.append(current)
                break
        else:
            adjacent = highest_adjacents(hm, path.path, current_char, adjacent_p)
            print(f"{adjacent=}")

            path.path.append(current)
            current = adjacent[0]

    path.path = path.path[1:]

    return path


def p1(fp: str) -> None:
    hm = load_heightmap(fp)
    start, end = find_char(hm, "S"), find_char(hm, "E")
    print(f"{start=}, {end=}")

    path = pathfind(hm, start, end)
    print(path.path)
    print(len(path.path))


def p2(fp: str) -> None:
    hm = load_heightmap(fp)


if __name__ == "__main__":
    fp = "samples/12.txt"
    # fp = "inputs/12.txt"

    p1(fp)
    p2(fp)
