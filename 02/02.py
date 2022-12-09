#! /usr/bin/env python3

# Advent of Code 22 - Day 2


def load_guide(fp: str) -> list[tuple[int, int]]:
    """
    Turns the text guide into tuples of `int`s, with
    `0` meaning `rock`, `1` meaning `paper` and `2` meaning scissors."""

    with open(fp, "r") as f:
        lines = f.readlines()

    conversions = {
        "A": 0,
        "B": 1,
        "C": 2,
        "X": 0,
        "Y": 1,
        "Z": 2,
    }
    plays = []

    for line in lines:
        p1, p2 = line.split()
        plays.append((conversions[p1], conversions[p2]))

    return plays


def get_score(play: tuple[int, int]) -> int:
    """
    Calculates the total amount of points earned in a round.

    Takes a tuple of `(p1, p2)` as input where `p1` and `p2` are `0`, `1` or `2`
    for rock, paper or scissors, respectively.
    """

    def get_winner(p1: int, p2: int) -> int:
        """
        Gets `0`, `1` or `2` for `rock`, `paper` or `scissors`, respectively, for both players.

        Returns `0` if p2 lost, `1` if it is a draw and `2` if p2 won.
        """

        if p1 == p2:
            return 1

        outcomes = {"01": 2, "02": 0, "10": 0, "12": 2, "20": 2, "21": 0}

        return outcomes[f"{p1}{p2}"]

    p1, p2 = play

    shape_score = p2 + 1
    outcome_score = 3 * get_winner(p1, p2)

    return shape_score + outcome_score


def get_play(play: tuple[int, int]) -> tuple[int, int]:
    """
    Takes a tuple of `0`, `1` or `2` for `rock`, `paper` or `scissors`, respectively, for `p1`
    and `0`, `1` or `2` for `lose`, `draw` or `win`, respectively.

    Returns `p2`'s play as `0`, `1` or `2` for `rock`, `paper` or `scissors`, respectively.
    """

    p1, outcome = play

    if outcome == 1:
        return p1, p1

    if outcome == 0:
        if p1 == 0:
            return p1, 2
        return p1, p1 - 1
    else:
        if p1 == 2:
            return p1, 0
        return p1, p1 + 1


def main(fp: str = "sample.txt"):
    # Part 1
    plays = load_guide(fp)
    scores = []
    for play in plays:
        scores.append(get_score(play))

    print(f"Total score is: {sum(scores)}")

    # Part 2
    plays = [(get_play(play)) for play in plays]
    scores = []
    for play in plays:
        scores.append(get_score(play))

    print(f"Total score with new interpretation is: {sum(scores)}")


if __name__ == "__main__":
    main("input.txt")
