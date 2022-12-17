#! /usr/bin/env python3

# Advent of Code 22 - Day 9

MOVE_UP = (-1, 0)
MOVE_DOWN = (1, 0)
MOVE_LEFT = (0, -1)
MOVE_RIGHT = (0, 1)


def load_instructions(fp: str) -> list[tuple[str, int]]:
    """Load the instructions from the file into `(direction, count)` tuples"""
    with open(fp, "r") as f:
        content = [(line.split()[0], int(line.split(" ")[1])) for line in f.readlines()]

    return content


def is_touching(head: tuple[int, int], tail: tuple[int, int]) -> bool:
    """Returns `True` if `tail` is in the 8 adjacent positions to `head`."""
    return abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1


def move_head(direction: str, head: tuple[int, int], count: int) -> tuple[int, int]:
    """Move the head following the direction."""

    movements = {
        "U": MOVE_UP,
        "D": MOVE_DOWN,
        "L": MOVE_LEFT,
        "R": MOVE_RIGHT,
    }

    movement = movements[direction]

    return tuple([head[i] + count * movement[i] for i in (0, 1)])


def move_tail(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    """Move the tail to follow the head"""

    move_u = (head[0] - tail[0]) <= -1
    move_d = (head[0] - tail[0]) >= 1
    move_l = (head[1] - tail[1]) <= -1
    move_r = (head[1] - tail[1]) >= 1

    # For y negative going up and x negative going left
    movement = [move_d - move_u, move_r - move_l]

    tail = tuple([tail[i] + movement[i] for i in range(2)])

    return tail


def move_rope(
    direction: str,
    count: int,
    head: tuple[int, int],
    tail: tuple[int, int],
    visited_coords: list[tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    head = move_head(direction, head, count)

    while not is_touching(head, tail):
        tail = move_tail(head, tail)
        if visited_coords:
            visited_coords.append(tuple(tail))

    return head, tail


def main(fp: str = "samples/09.txt"):
    instructions = load_instructions(fp)

    # Part 1
    head = (0, 0)
    tail = (0, 0)

    visited_coords = [(0, 0)]

    for instruction in instructions:
        direction, count = instruction
        head, tail = move_rope(direction, count, head, tail, visited_coords)

    visited_places_count = len(set(visited_coords))

    # Length without duplicates
    print("Visited coords:", visited_places_count)
    print("End:", fp, head, tail)

    # # Part 2
    # visited_coords = [(0, 0)]

    # segment_count = 10
    # segments: list[tuple[int, int]] = [(0, 0) for _ in range(segment_count)]

    # for instruction in instructions:
    #     direction, count = instruction
    #     for i in range(segment_count - 1):
    #         segments[i], segments[i + 1] = move_rope(
    #             direction,
    #             count,
    #             segments[i],
    #             segments[i + 1],
    #             visited_coords if segments[i] is segments[8] else None,
    #         )

    # visited_places_count = len(set(visited_coords))

    # # Length without duplicates
    # print("Visited coords:", visited_places_count)
    # print(visited_coords)
    # print("End:", fp, head, tail)


if __name__ == "__main__":
    main()
    main("inputs/09.txt")  # 6256
    # main("09/sample2.txt")
