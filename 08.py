#! /usr/bin/env python3

# Advent of Code 22 - Day 8


def load_trees(fp: str) -> list[list[int]]:
    """Load the trees from a file to a matrix"""

    with open(fp, "r") as f:
        content = [[int(i) for i in line.strip()] for line in f.readlines()]

    return content


def is_visible(trees: list[list[int]], row: int, col: int) -> bool:
    """
    Returns `True` if the tree in `trees[row][col]` is taller than
    all other trees in a straight line from it to the any border.
    """

    rows = len(trees)
    cols = len(trees[0])

    if row == 0 or col == 0 or row == rows or col == cols:  # Edges are always visible
        return True

    top = all([trees[row][col] > trees[i][col] for i in range(0, row) if i != row])
    right = all([trees[row][col] > trees[row][i] for i in range(col, cols) if i != col])
    bottom = all(
        [trees[row][col] > trees[i][col] for i in range(row, rows) if i != row]
    )
    left = all([trees[row][col] > trees[row][i] for i in range(0, col) if i != col])

    return top or bottom or left or right


def scenic_score(trees: list[list[int]], row: int, col: int) -> int:
    """
    Returns the amount of trees visible from a specific tree.
    """

    rows = len(trees)
    cols = len(trees[0])

    if row == 0 or col == 0 or row == rows - 1 or col == cols - 1:
        return 0  # Edges have at least one 0 distance, so any product is 0

    top = right = bottom = left = 0
    for i in range(row, -1, -1):
        if i != row:
            if trees[row][col] > trees[i][col]:
                top += 1
            else:
                top += 1
                break
    for i in range(col, cols):
        if i != col:
            if trees[row][col] > trees[row][i]:
                right += 1
            else:
                right += 1
                break
    for i in range(row, rows):
        if i != row:
            if trees[row][col] > trees[i][col]:
                bottom += 1
            else:
                bottom += 1
                break
    for i in range(col, -1, -1):
        if i != col:
            if trees[row][col] > trees[row][i]:
                left += 1
            else:
                left += 1
                break

    return top * bottom * left * right


def main(fp: str = "samples/08.txt"):
    # Part 1
    trees = load_trees(fp)

    is_visible_matrix = [list() for _ in trees]
    for row in range(len(trees)):
        for col in range(len(trees[0])):
            is_visible_matrix[row].append(is_visible(trees, row, col))

    print(sum([sum(row) for row in is_visible_matrix]))

    # Part 2
    scenic_score_matrix = [list() for _ in trees]
    for row in range(len(trees)):
        for col in range(len(trees[0])):
            scenic_score_matrix[row].append(scenic_score(trees, row, col))

    print(max([max(row) for row in scenic_score_matrix]))


if __name__ == "__main__":
    main("inputs/08.txt")
