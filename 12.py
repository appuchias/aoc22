#! /usr/bin/env python3

# Advent of Code 22 - Day 12

from typing import List, Callable
from dataclasses import dataclass, field
from time import sleep

from models import Point


def load_heightmap(fp: str) -> tuple[List[List[int]], Point, Point]:
    with open(fp, "r") as f:
        lines = f.readlines()
        start = lines.index([line for line in lines if "S" in line][0])
        start = Point(lines[start].index("S"), start)
        end = lines.index([line for line in lines if "E" in line][0])
        end = Point(lines[end].index("E"), end)

        content = [
            [ord(c.replace("S", "a").replace("E", "z")) - ord("a") for c in line]
            for line in lines
        ]

    return content, start, end


@dataclass(frozen=True, order=True)
class Node:
    point: Point = field(compare=False)
    height: int = field(compare=False)
    distance: float = field(default=float("inf"), compare=True)
    previous: Point = field(default=Point(-1, -1))


def get_height(hm: List[List[int]], p: Point) -> int:
    """Returns the relative height of a point (`p`)"""
    return hm[p.y][p.x]


def get_valid_neighbors(
    hm: List[List[int]], n: Node, s: List[Node], c: List[Node]
) -> List[Point]:
    """
    Returns a `list` of the adjacent points that
    can be visited from the current one
    """

    def is_valid(p: Point) -> bool:
        """
        Returns `True` if `p` is in the board, it is reachable
        and it hasn't been visited before
        """

        # Check if point in board
        if not any([p.x < 0, p.y < 0, p.x > len(hm[0]) - 1, p.y > len(hm) - 1]):
            # Check if it a reachable unvisited point
            return (
                get_height(hm, p) - p_height <= 1
                and p not in [n.point for n in s]
                and p not in [n.point for n in c]
            )
        return False

    p_height = get_height(hm, n.point)

    # Remove invalid adjacent points
    return list(filter(is_valid, n.point.get_adjacent()))


def backtrack(completed: list[Node], path: List[Point], start: Point) -> List[Point]:
    while path[-1] != start:
        for node in completed:
            if node.point == path[-1]:
                path.append(node.previous)

    return path


def dijkstra(hm: List[List[int]], start: Point, end: Point) -> List[Point]:
    """
    Get the shortest path between `start` and `end` following the heightmap `hm`.

    You can only go up one step but there is no limit going down
    """

    stack = [Node(start, 0, 0)]
    completed = list()
    path: List[Point] = [end]

    # Loop until no positions left to analyze
    while stack:
        node = stack[0]
        height = get_height(hm, node.point)

        if node == end:  # Currently useless but needs a rework
            stack.append(Node(end, ord("z"), 0, completed[-1]))
            continue

        neighbors = get_valid_neighbors(hm, node, stack, completed)
        heights = [get_height(hm, i) for i in neighbors]

        # Get iterable of (distance, height, Point) tuples
        # distance = new_height - old_height
        neighbors_distance_height = filter(
            lambda x: x[0] <= 1,
            zip(map(lambda x: x - height, heights), heights, neighbors),
        )

        # Sort by highest distance (highest height delta)
        neighbors = sorted(
            map(
                lambda x: Node(x[2], x[0], x[1], node.point), neighbors_distance_height
            ),
            reverse=True,
        )

        for neighbor in neighbors:
            stack.append(neighbor)

        completed.append(stack.pop(0))

        print_board(hm, completed, path, end)

    path = backtrack(completed, path, start)

    print_board(hm, completed, path, end)

    return path[1:]


def print_board(hm, stack, path, end) -> None:
    board = [[" " for _ in hm[0]] for _ in hm]
    # board = [[chr(i) for i in line] for line in hm]
    for p in [node.point for node in stack]:
        # board[p.y][p.x] = f"\033[1m{chr(hm[p.y][p.x] + 97)}\033[0m"
        board[p.y][p.x] = f"{chr(hm[p.y][p.x] + 97)}"
    for p in path:
        # board[p.y][p.x] = f"\033[1m{board[p.y][p.x].upper()}\033[0m"
        board[p.y][p.x] = "·"
    board[end.y][end.x] = "#"
    board = "\n".join([":".join(line).strip("\n") for line in board if line])

    print("\n" * 10)
    print(board)


def p1(fp: str) -> None:
    hm, start, end = load_heightmap(fp)

    path = dijkstra(hm, start, end)

    path = list(dict.fromkeys(path))

    # print(path)
    print()
    print(len(path))


def p2(fp: str) -> None:
    hm, start, end = load_heightmap(fp)

    # Run the algorithm in reverse to find closest `a` to E
    # Hard to do with the code as I have it as of now.


if __name__ == "__main__":
    fp = "samples/12.txt"
    fp = "inputs/12.txt"

    p1(fp)
    # p2(fp)
