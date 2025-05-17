#!/usr/bin/env python3

from string import ascii_lowercase
import pandas as pd

"""
sample words according to probability
eliminate words where characters don't exist
eliminate words where characters are in the wrong position

prioritize words with no duplicate characters?
"""

CORRECT = "c"
PRESENT = "p"
ABSENT = "a"

possibilities = {}

for idx in range(5):
    possibilities[idx] = set(list(ascii_lowercase))


def sample_word(df):
    return df["word"].loc[df["count"].idxmax()]


def eliminate(df, character, index, status):
    if status == CORRECT:
        return eliminate_correct(df, character, index)
    if status == PRESENT:
        return eliminate_present(df, character, index)
    if status == ABSENT:
        return eliminate_absent(df, character, index)
    raise ValueError("invalid status")


def eliminate_correct(df, character, index):
    def _eliminate_correct(word):
        return word[index] == character

    mask = df["word"].apply(_eliminate_correct)
    return df[mask]


def eliminate_present(df, character, index):
    def _eliminate_present(word):
        return character in word

    mask = df["word"].apply(_eliminate_present)
    df = df[mask]

    def _eliminate_position(word):
        return word[index] != character

    mask = df["word"].apply(_eliminate_position)
    return df[mask]


def eliminate_absent(df, character, index):
    def _eliminate_absent(word):
        return character not in word

    mask = df["word"].apply(_eliminate_absent)
    return df[mask]


def get_result(word):
    print(f"guess:  {word}")
    return input("status (c:correct, p:present, a:absent) or remove > ").lower()


def remove_word(df, word):
    mask = df["word"] != word
    return df[mask]


def solve():
    df = pd.read_csv("5_letter_words.csv")
    idx = 0

    while idx < 6:
        word = sample_word(df)
        result = get_result(word)

        if "remove" == result:
            df = remove_word(df, word)
            continue

        for jdx, (character, status) in enumerate(zip(word, result)):
            df = eliminate(df, character, jdx, status)

        idx += 1


if __name__ == "__main__":
    solve()
