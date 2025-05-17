import unittest
from unittest.mock import patch
from pprint import pprint
import pandas as pd
import wordle_solver as ws


class TestWordleSolver(unittest.TestCase):

    with open("previous_wordles.txt") as f_in:
        wordles = f_in.readlines()

    wordles = list(map(lambda x: x.strip().lower(), wordles))

    def test_solve_distribution(self):
        guess_counts = {}

        for wordle in self.wordles:
            print(wordle)
            guess_counts[wordle] = self.get_guess_count(wordle)

        guess_counts = pd.DataFrame(guess_counts.items(), columns=["word", "guesses"])
        guess_counts = guess_counts.set_index("word", drop=True)
        print(guess_counts)

        value_counts = guess_counts.value_counts()
        print(value_counts.sort_index())
        breakpoint()

    @patch.object(ws, "get_result")
    def get_guess_count(self, wordle, mock_get_result):
        guess_count = 0

        def get_result(guess):
            # print(guess)
            return self._get_result(guess, wordle)

        mock_get_result.side_effect = get_result
        ws.solve()

        guesses = [call_args.args[0] for call_args in mock_get_result.call_args_list]

        try:
            return 1 + guesses.index(wordle)
        except ValueError:
            return -1

    def _get_result(self, guess, wordle):
        result = ""

        for idx, (guess_, wordle_) in enumerate(zip(guess, wordle)):
            if guess_ == wordle_:
                result += "c"

            elif guess_ in wordle:
                result += "p"

            else:
                result += "a"

        return result
