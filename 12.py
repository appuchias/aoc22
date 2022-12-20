#! /usr/bin/env python3

# Advent of Code 22 - Day 12

from typing import List
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


def is_in_board(hm: List[List[int]], p: Point) -> bool:
    return not any([p.x < 0, p.y < 0, p.x > len(hm[0]) - 1, p.y > len(hm) - 1])


def get_valid_neighbors(
    hm: List[List[int]], n: Node, s: List[Node], c: List[Node]
) -> List[Point]:
    def is_valid(a: Point) -> bool:
        if is_in_board(hm, a):
            return (
                get_height(hm, a) - get_height(hm, n.point) <= 1
                and a not in [n.point for n in s]
                and a not in [n.point for n in c]
            )
        return False

    return list(filter(is_valid, n.point.get_adjacent()))


def dijkstra(hm: List[List[int]], start: Point, end: Point) -> List[Point]:
    stack = [Node(start, 0, 0)]
    completed = list()

    # Loop until end is reached
    while stack:
        node = stack[0]
        height = get_height(hm, node.point)

        if node == end:
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
        print(f"{stack=}")

        print_board(hm, completed, end)
        sleep(0.01)
        # input()

    path: List[Point] = [end]
    while path[-1] != start:
        for node in completed:
            if node.point == path[-1]:
                path.append(completed.pop(completed.index(node)).previous)

    # return [n.point for n in completed]
    return path


def p1(fp: str) -> None:
    hm, start, end = load_heightmap(fp)

    path = dijkstra(hm, start, end)

    path = list(dict.fromkeys(path))

    print(path)
    print(len(path) - 1)


def p2(fp: str) -> None:
    _ = load_heightmap(fp)


def print_board(hm, stack, end) -> None:
    board = [[" " for _ in hm[0]] for _ in hm]
    # board = [[chr(i) for i in line] for line in hm]
    for p in [node.point for node in stack]:
        board[p.y][p.x] = f"\033[1m{chr(hm[p.y][p.x] + 97)}\033[0m"
    board[end.y][end.x] = "#"
    board = "\n".join(["·".join(line) for line in board if line])

    print(board)


if __name__ == "__main__":
    fp = "samples/12.txt"
    fp = "inputs/12.txt"

    p1(fp)
    p2(fp)

    #     nodes = stack.sort_nodes().copy()

    #     if nodes[point].point == end:
    #         finished = True
    #         continue

    #     for node in nodes:
    #         if not is_in_board(hm, node.point):
    #             continue

    #         adjacent = sorted(
    #             get_valid_neighbors(hm, node.point, stack),
    #             key=lambda p: get_height(hm, p),
    #             reverse=True,
    #         )

    #         for point in adjacent:
    #             height = get_height(hm, point)
    #             print(f"{point=}, {height=}")
    #             new_node = Node(point, height, distance(point, start))
    #             new_node.set_previous(node)
    #             stack.nodes[point] = new_node

    #         stack.completed[node.point] = stack.nodes[node.point]
    #         del stack.nodes[node.point]
