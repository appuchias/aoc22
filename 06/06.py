#! /usr/bin/env python3

# Advent of Code 22 - Day 6


def read_datastream(fp: str) -> list[str]:
    """Reads the datastream (one or multiple lines)"""
    with open(fp, "r") as f:
        content = [line.strip() for line in f.readlines()]

    return content


def find_start(ds: str, n: int) -> int:
    """
    Finds the first `n` consecutive different characters in the datastream and
    returns the index of the last one.
    """

    for i in range(0, len(ds)):
        segment = ds[i : n + i]
        if len(dict.fromkeys(segment)) == n:
            return n + i

    return -1


def main(fp: str = "06/sample.txt"):
    # Part 1
    ds = read_datastream(fp)

    for line in ds:
        start = find_start(line, 4)
        print(start)

    # Part 2
    for line in ds:
        start = find_start(line, 14)
        print(start)


if __name__ == "__main__":
    main("06/input.txt")
