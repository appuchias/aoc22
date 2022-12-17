#! /usr/bin/env python3

# Advent of Code 22 - Day 7


from typing import Iterable


def load_commands(fp: str) -> list[str]:
    with open(fp, "r") as f:
        content = [line.strip() for line in f.readlines()]

    return content


def build_tree(commands: list[str]) -> dict:
    """
    Builds the directory tree, where directories have a `dict` value
    and files have an `int` value representing their size.
    """

    tree = dict()

    # tree = {
    #     "dir1": {
    #         "dir2": {
    #             "file3": 1000,
    #         },
    #         "file2": 3000,
    #     },
    #     "file1": 2000,
    # }

    current_path = list()

    for command in commands:
        command = command.split(" ")  # Make ir easier to find arguments

        if command[0] == "$":  # Moving or listing
            if command[1] == "cd":  # cd
                if command[2] == "..":  # cd ..
                    current_path.pop(-1)
                else:  # cd <dir>
                    current_path.append(command[2])
            else:  # ls
                pass

        else:  # Adding files/dirs
            if command[0] == "dir":  # Add a dir
                parent = tree
                for key in current_path[1:]:
                    parent = parent[key]
                parent[command[1]] = dict()
            else:  # Add a file
                parent = tree
                for key in current_path[1:]:
                    parent = parent[key]
                parent[command[1]] = int(command[0])

    return tree


def size(tree: dict) -> int:
    """
    Walk through `tree` and return the sum of
    the sizes of all items contained in it.
    """

    total_size = 0

    for v in tree.values():
        if isinstance(v, dict):
            total_size += size(v)
        else:
            total_size += v

    return total_size


def find_dict_sizes(tree: dict) -> Iterable[int]:
    """
    Returns an iterable of the size of every dict in the tree.
    """
    for v in tree.values():
        if isinstance(v, dict):
            yield size(v)
            for i in find_dict_sizes(v):
                if i:
                    yield i


def main(fp: str = "samples/07.txt"):
    # Part 1
    commands = load_commands(fp)
    tree = build_tree(commands)

    # import json
    # with open("07/tmp.json", "w") as w:
    #     json.dump(tree, w, indent=4, sort_keys=True)

    sizes = list(find_dict_sizes(tree))
    print(sum(filter(lambda x: x < 100000, sizes)))

    # Part 2
    total_size = 70_000_000
    min_free = 30_000_000

    size_currently_free = total_size - size(tree)
    size_to_free = min_free - size_currently_free

    print(min(filter(lambda x: x > size_to_free, sizes)))


if __name__ == "__main__":
    main("inputs/07.txt")
