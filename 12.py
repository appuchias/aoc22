#! /usr/bin/env python3

# Advent of Code 22 - Day 12

from typing import List
from models import Point


def load_heightmap(fp: str) -> List[str]:
    with open(fp, "r") as f:
        content = [line.strip() for line in f.readlines()]

    return content


def find_char(heightmap: List[str], char: str) -> Point:
    p1 = heightmap.index([line for line in heightmap if char in line][0])
    return Point(p1, heightmap[p1].index(char))


def point_in_hm(heightmap: List[str], p: Point) -> bool:
    boundaries = [
        p.x < 0,
        p.y < 0,
        p.x > len(heightmap) - 1,
        p.y > len(heightmap[0]) - 1,
    ]
    return not any(boundaries)


def find_path_recursive(
    heightmap: List[str],
    start: Point,
    end: Point,
    path: List[Point],
) -> List[Point]:
    prev = path[-1]
    if start not in path:
        path.append(start)
    start_char = heightmap[start.x][start.y].replace("S", "a")

    for point in sorted(
        start.get_adjacent(),
        key=lambda p: ord(heightmap[p.x][p.y]) if point_in_hm(heightmap, p) else 0,
        reverse=True,
    ):
        # if not point_in_hm(heightmap, point):
        #     continue

        current_char = heightmap[point.x][point.y].replace("E", "z")
        if point == end and ord(current_char) - ord(start_char) <= 1:
            return path

        height_delta = ord(current_char) - ord(start_char)
        if height_delta in [0, 1] and point != prev:
            # print(f"Δ={height_delta} ({point})")
            find_path_recursive(heightmap, point, end, path)
            break

    return path


def p1_recursive(fp: str):
    heightmap = load_heightmap(fp)
    start, end = find_char(heightmap, "S"), find_char(heightmap, "E")

    # heightmap[start.x] = heightmap[start.x].replace("S", "a")
    # heightmap[end.x] = heightmap[end.x].replace("E", "z")

    path = find_path_recursive(heightmap, start, end, [start])

    board = [["." for _ in heightmap[0]] for _ in heightmap]
    for p in path:
        board[p.x][p.y] = heightmap[p.x][p.y]
    board[end.x][end.y] = " "

    from pprint import pprint

    pprint(board)

    print(len(path))


if __name__ == "__main__":
    fp = "samples/12.txt"
    # fp = "inputs/12.txt"

    p1_recursive(fp)
