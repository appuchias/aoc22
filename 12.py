#! /usr/bin/env python3

# Advent of Code 22 - Day 12

from typing import List
from models import Point, distance
from dataclasses import dataclass, field

from time import sleep
from random import sample


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


def parse_hm(hm: List[str]) -> List[List[int]]:
    return [
        [ord(char.replace("S", "a").replace("E", "z")) for char in line.strip()]
        for line in hm
    ]


def find_char(heightmap: List[str], char: str) -> Point:
    p1 = heightmap.index([line for line in heightmap if char in line][0])
    return Point(heightmap[p1].index(char), p1)


def point_in_hm(heightmap: List[List[int]], p: Point) -> bool:
    boundaries = [
        p.x < 0,
        p.y < 0,
        p.x > len(heightmap[0]) - 1,
        p.y > len(heightmap) - 1,
    ]
    return not any(boundaries)


def highest_adjacents(
    hm: List[List[int]],
    path: List[Point],
    current_ord: int,
    adjacent_p: List[Point],
    end: Point,
) -> List[Point]:

    # Remove points outside hm and points in current path
    adjacent_p = list(
        filter(
            None,
            [p for p in adjacent_p if point_in_hm(hm, p) and p not in path],
        )
    )

    print(f"{adjacent_p=}")

    # Get highest delta meeting 0<=Δ<=1
    deltas = list(
        filter(
            lambda t: 0 <= t[0] <= 1,
            map(
                lambda x, y: (x - current_ord, y),
                [hm[p.y][p.x] for p in adjacent_p],
                adjacent_p,
            ),
        )
    )

    if len(deltas) == 0:
        return list()

    delta = max(deltas)[0]
    print(f"{deltas=}, {delta=}")

    # Remove points with lower deltas
    adjacent = [i[1] for i in filter(lambda t: t[0] == delta, deltas)]
    print(f"{adjacent=}")

    # Sort by smallest distance
    adjacent = sorted(
        map(lambda p: (distance(p, end), p), adjacent),
        reverse=False,
        key=lambda t: t[0],
    )
    print(f"{adjacent=}")

    return [i[1] for i in adjacent]

    return sample(adjacent, k=len(adjacent))


def pathfind(hm: List[List[int]], start: Point, end: Point) -> Path:
    """Find all paths to go from `start` to `end` following the heightmap (`hm`)."""

    finished = False
    path: Path = Path(start, end, [start])
    dead_ends = set()

    current = start

    while not finished:
        current_ord = hm[current.y][current.x]

        adjacent_p: List[Point] = current.get_adjacent()

        for p in adjacent_p:
            if p == end and (ord("z") - current_ord <= 1):
                finished = True
                path.path.append(current)
                print()
                break
        else:
            adjacent = highest_adjacents(hm, path.path, current_ord, adjacent_p, end)
            adjacent = list(filter(lambda p: p not in dead_ends, adjacent))
            print(f"{current=}, {adjacent=}")

            if len(adjacent) == 0:
                prev = path.path.pop(-1)
                dead_ends.add(current)
                current = prev
            else:
                path.path.append(current)
                current = adjacent[0]

        print_board(hm, path.path, end)
        # input()
        sleep(0.005)

    path.path = path.path[1:]

    return path


def print_board(hm, path, end) -> None:
    board = [[" " for _ in hm[0]] for _ in hm]
    # board = [[chr(i) for i in line] for line in hm]
    for p in path:
        board[p.y][p.x] = "\033[1m" + chr(hm[p.y][p.x]).upper() + "\033[0m"
    board[end.y][end.x] = "#"
    board = "\n".join(["·".join(line) for line in board])

    print(board)


def p1(fp: str) -> None:
    str_hm = load_heightmap(fp)
    start, end = find_char(str_hm, "S"), find_char(str_hm, "E")
    print(f"{start=}, {end=}")

    hm = parse_hm(str_hm)
    path = pathfind(hm, start, end)

    # print(path.path)
    print(len(path.path))


def p2(fp: str) -> None:
    hm = load_heightmap(fp)


if __name__ == "__main__":
    fp = "samples/12.txt"
    fp = "inputs/12.txt"

    p1(fp)
    p2(fp)
