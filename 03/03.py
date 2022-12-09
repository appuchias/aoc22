#! /usr/bin/env python3

# Advent of Code 22 - Day 3


def load_rucksacks(fp: str) -> list[tuple[str, str]]:
    """
    Get rucksacks from file and return them as a list of tuples.
    Each tuple contains the items of both compartments separated.
    """

    with open(fp, "r") as f:
        rucksacks = f.readlines()

    rucksacks_in_compartments = []
    for rucksack in rucksacks:
        half = len(rucksack) // 2
        compartments = (rucksack[:half], rucksack[half:])
        rucksacks_in_compartments.append(compartments)

    return rucksacks_in_compartments


def get_common_items(rucksack: tuple[str, str]) -> str:
    """Returns the items shared between both compartments"""

    c1, c2 = rucksack
    for item in c1:
        if item in c2:
            # At most 1 item in common per rucksack
            return item

    return ""


def get_item_priority(item: str) -> int:
    """
    Returns the priority of an item. `1-26` for
    lowercase letters and `27-52` for uppercase.
    """
    if item == item.lower():
        return ord(item.upper()) - 64  # 1 -  26
    return ord(item.lower()) - 70  # 27 - 52


def get_badges(rucksacks: list[tuple[str, str]], n: int = 3) -> list[str]:
    """Returns a list of the items shared between every group of `n` elves."""

    common_items = []
    for i in range(len(rucksacks) // n):
        rucksack = rucksacks[i * n]
        content = rucksack[0] + rucksack[1]
        for char in content:
            group = [
                rucksacks[i * n + j][0] + rucksacks[i * n + j][1] for j in range(1, n)
            ]
            if all([char in rucksack for rucksack in group]):
                common_items.append(char)
                break

    return common_items


def main(fp: str = "sample.txt"):
    # Part 1
    rucksacks = load_rucksacks(fp)
    common_items = list(map(get_common_items, rucksacks))
    priorities = list(map(get_item_priority, common_items))
    print(f"Total common items priority is: {sum(priorities)}")

    # Part 2
    badges = get_badges(rucksacks)
    priorities = list(map(get_item_priority, badges))
    print(f"Total badge priority is: {sum(priorities)}")


if __name__ == "__main__":
    # main()
    main("input.txt")
