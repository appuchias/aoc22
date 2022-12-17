#! /usr/bin/env python3

# Advent of Code 22 - Day 4


def load_assignments(fp: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """
    Returns a list of tuples containing the range of each elf (as a tuple).
    """

    with open(fp, "r") as f:
        assignments = [line.strip() for line in f.readlines()]

    output = []
    for assignment in assignments:
        a1, a2 = assignment.split(",")
        a1 = tuple([int(i) for i in a1.split("-")])
        a2 = tuple([int(i) for i in a2.split("-")])
        output.append((a1, a2))

    return output


def is_assignment_contained(
    assignment: tuple[tuple[int, int], tuple[int, int]]
) -> bool:
    """
    Returns `True` if one element of `assignment` is fully contained in the other one.
    """

    a1, a2 = assignment

    a1_in_a2 = a1[0] >= a2[0] and a1[1] <= a2[1]
    a2_in_a1 = a2[0] >= a1[0] and a2[1] <= a1[1]

    return a1_in_a2 or a2_in_a1


def is_overlapped(assignment: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    """
    Returns `True` if  one of the assignments overlaps the other one.
    """

    a1, a2 = assignment

    range1 = range(a1[0], a1[1] + 1)
    range2 = range(a2[0], a2[1] + 1)

    # This could work like is_assignment_contained if you swap `any` for `all`
    return any([i in range2 for i in range1]) or any([i in range1 for i in range2])


def main(fp: str = "04/sample.txt"):
    # Part 1
    assignments = load_assignments(fp)
    contained = list(map(is_assignment_contained, assignments))

    print(f"Number of assignments contained: {contained.count(True)}")

    # Part 2
    overlaps = list(map(is_overlapped, assignments))
    print(f"The amount of assignments with overlaps is: {overlaps.count(True)}")


if __name__ == "__main__":
    # main()
    main("04/input.txt")
