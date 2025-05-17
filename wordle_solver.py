#!/usr/bin/env python3

from collections import defaultdict
from string import ascii_lowercase
import pandas as pd

"""
sample words according to probability
prioritize words with no duplicate characters?
eplore/exploit ratio?
  - use first guesses to eliminate characters
  - use later guesses to attempt a solve
"""

CORRECT = "c"
PRESENT = "p"
ABSENT = "a"


class AutoWordler:

    def __init__(self):
        self.vocabulary = pd.read_csv("5_letter_words.csv")

    def sample_word(self, df):
        """
        Return the most likely word from the candidates.
        """
        return df["word"].loc[df["count"].idxmax()]

    def eliminate(self, df, result, word):
        """
        Eliminate words based on wordle feedback.
        """
        word_value_counts = defaultdict(lambda: 0)

        for idx, (character, status) in enumerate(zip(word, result)):
            if status == CORRECT:
                df = self.eliminate_correct(df, character, idx)
                word_value_counts[character] += 1

        for idx, (character, status) in enumerate(zip(word, result)):
            if status == PRESENT:
                df = self.eliminate_present(df, character, idx)
                df = self.eliminate_position(df, character, idx)
                word_value_counts[character] += 1

            if status == ABSENT:
                # eliminate words with the character in any position
                if word_value_counts[character] == 0:
                    df = self.eliminate_absent(df, character, idx)

                # eliminate words with the character in the specified position
                if word_value_counts[character] >= 0:
                    df = self.eliminate_position(df, character, idx)

        return df

    def eliminate_position(self, df, character, index):
        """
        Eliminate words where the character is present in the specified index.
        """

        def _eliminate_position(word):
            return word[index] != character

        mask = df["word"].apply(_eliminate_position)
        return df[mask]

    def eliminate_correct(self, df, character, index):
        """
        Eliminate words which don't have the character in the specified index.
        """

        def _eliminate_correct(word):
            return word[index] == character

        mask = df["word"].apply(_eliminate_correct)
        return df[mask]

    def eliminate_present(self, df, character, index):
        """
        Remove words which don't contain character.
        """

        def _eliminate_present(word):
            return character in word

        mask = df["word"].apply(_eliminate_present)
        return df[mask]

    def eliminate_absent(self, df, character, index):
        """
        Eliminate words which contain the specified character.
        """

        def _eliminate_absent(word):
            return character not in word

        mask = df["word"].apply(_eliminate_absent)
        return df[mask]

    def get_result(self, word):
        """
        Collect feedback for a guess.
        """
        print(f"guess:  {word}")
        return input("status (c:correct, p:present, a:absent) or remove > ").lower()

    def remove_word(self, df, word):
        """
        Remove a specific word:  useful for skipping unlikely words like https/xhtml/etc.
        """
        mask = df["word"] != word
        return df[mask]

    def solve(self):
        df = self.vocabulary.copy()
        idx = 0

        while idx < 6:
            word = self.sample_word(df)
            result = self.get_result(word)

            if "remove" == result:
                df = self.remove_word(df, word)
                continue

            df = self.eliminate(df, result, word)
            idx += 1


if __name__ == "__main__":
    AutoWordler().solve()
