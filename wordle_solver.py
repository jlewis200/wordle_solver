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

    def sample_word(self):
        """
        Return the most likely word from the candidates.
        """
        return self.df["word"].loc[self.df["count"].idxmax()]

    def eliminate(self, result, word):
        """
        Eliminate words based on wordle feedback.
        """
        word_value_counts = defaultdict(lambda: 0)

        for idx, (character, status) in enumerate(zip(word, result)):
            if status == CORRECT:
                self.eliminate_correct(character, idx)
                word_value_counts[character] += 1

        for idx, (character, status) in enumerate(zip(word, result)):
            if status == PRESENT:
                self.eliminate_present(character, idx)
                self.eliminate_position(character, idx)
                word_value_counts[character] += 1

            if status == ABSENT:
                # eliminate words with the character in any position
                if word_value_counts[character] == 0:
                    self.eliminate_absent(character, idx)

                # eliminate words with the character in the specified position
                if word_value_counts[character] >= 0:
                    self.eliminate_position(character, idx)

    def eliminate_position(self, character, index):
        """
        Eliminate words where the character is present in the specified index.
        """

        def _eliminate_position(word):
            return word[index] != character

        mask = self.df["word"].apply(_eliminate_position)
        self.df = self.df[mask]

    def eliminate_correct(self, character, index):
        """
        Eliminate words which don't have the character in the specified index.
        """

        def _eliminate_correct(word):
            return word[index] == character

        mask = self.df["word"].apply(_eliminate_correct)
        self.df = self.df[mask]

    def eliminate_present(self, character, index):
        """
        Remove words which don't contain character.
        """

        def _eliminate_present(word):
            return character in word

        mask = self.df["word"].apply(_eliminate_present)
        self.df = self.df[mask]

    def eliminate_absent(self, character, index):
        """
        Eliminate words which contain the specified character.
        """

        def _eliminate_absent(word):
            return character not in word

        mask = self.df["word"].apply(_eliminate_absent)
        self.df = self.df[mask]

    def get_result(self, word):
        """
        Collect feedback for a guess.
        """
        print(f"guess:  {word}")
        return input("status (c:correct, p:present, a:absent) or remove > ").lower()

    def remove_word(self, word):
        """
        Remove a specific word:  useful for skipping unlikely words like https/xhtml/etc.
        """
        mask = self.df["word"] != word
        self.df = self.df[mask]

    def solve(self):
        self.df = self.vocabulary.copy()
        idx = 0

        while idx < 6:
            word = self.sample_word()
            result = self.get_result(word)

            if "remove" == result:
                df = self.remove_word(word)
                continue

            self.eliminate(result, word)
            idx += 1


if __name__ == "__main__":
    AutoWordler().solve()
