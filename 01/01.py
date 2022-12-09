#! /usr/bin/env python3

# Advent of Code 22 - Day 1


def get_elves(fp: str) -> list[list[int]]:
    """
    Get calories carried by elves from `fp` and return them
    as a list of the list of calories carried by every elf.
    """

    elves = []

    with open(fp, "r") as f:
        for elf in f.read().split("\n\n"):
            elves.append([int(line) for line in elf.splitlines()])
    return elves


def get_heaviest_elf_idx_and_calories(elves: list[list[int]]) -> tuple[int, int]:
    """
    Get the elf carrying the most calories and the total amount of calories carried by them.
    """

    calories = []

    for elf in elves:
        calories.append(sum(elf))

    return calories.index(max(calories)), max(calories)


def get_top_elves_calories(elves: list[list[int]], n: int = 3) -> list[int]:
    """
    Get the total calories carried by the `n` elves carrying the most calories.
    """

    top = []

    calories = [sum(elf) for elf in elves]

    for _ in range(n):
        top.append(calories.pop(calories.index(max(calories))))

    return top


def main(fp: str = "sample.txt"):
    # Part 1
    elves = get_elves(fp)
    heaviest_elf_idx, heaviest_elf_calories = get_heaviest_elf_idx_and_calories(elves)
    print(
        "Elf #"
        + str(heaviest_elf_idx + 1)
        + " has the heaviest calories of "
        + str(heaviest_elf_calories)
    )

    # Part 2
    top_three = get_top_elves_calories(elves, 3)

    print(f"Top three elves carry a total of {sum(top_three)} calories")


if __name__ == "__main__":
    input_file = "input.txt"
    main(input_file)
