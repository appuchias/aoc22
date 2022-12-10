import os, sys


def create_day(day: str) -> None:
    content = f"""\
#! /usr/bin/env python3

# Advent of Code 22 - Day {int(day)}


def load_(fp: str) -> ...:
    with open(fp, "r") as f:
        content = f.read()


def main(fp: str = "{day}/sample.txt"):
    # Part 1
    ...

    # Part 2
    ...


if __name__ == "__main__":
    main()
"""

    os.mkdir(day)
    with open(f"{day}/{day}.py", "w") as f:
        f.write(content)
    open(f"{day}/input.txt", "x").close()
    open(f"{day}/sample.txt", "x").close()


if __name__ == "__main__":
    assert len(sys.argv) >= 2, "Please provide a day number"

    day = sys.argv[1]

    create_day(day)
