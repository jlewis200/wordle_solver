from collections import defaultdict
import unittest
from unittest.mock import patch
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import wordle_solver as ws
from plotting_utils import get_numeric_histogram


class TestWordleSolver(unittest.TestCase):

    with open("previous_wordles.txt") as f_in:
        wordles = f_in.readlines()

    wordles = list(map(lambda x: x.strip().lower(), wordles))

    def test_solve_distribution(self):
        """
        Generate a distribution of guesses-to-solve.
        """
        guess_counts = {}
        auto_wordler = ws.AutoWordler()

        for wordle in self.wordles:
            print(wordle)
            guess_counts[wordle] = self.get_guess_count(wordle, auto_wordler)

        guess_counts = pd.DataFrame(guess_counts.items(), columns=["word", "guesses"])
        guess_counts = guess_counts.set_index("word", drop=True)

        guess_counts = guess_counts.rename(
            columns={"guesses": "guess_count_distribution"}
        )
        fig, *_ = get_numeric_histogram(
            guess_counts["guess_count_distribution"],
            bins=[
                -1.4,
                -0.6,
                -0.4,
                0.4,
                0.6,
                1.4,
                1.6,
                2.4,
                2.6,
                3.4,
                3.6,
                4.4,
                4.6,
                5.4,
                5.6,
                6.4,
            ],
        )

        plt.savefig("guess_distribution.png")

    @patch.object(ws.AutoWordler, "get_result")
    def get_guess_count(self, wordle, auto_wordler, mock_get_result):
        mock_get_result.side_effect = lambda guess: get_result(guess, wordle)
        auto_wordler.solve()
        guesses = [call_args.args[0] for call_args in mock_get_result.call_args_list]

        try:
            return 1 + guesses.index(wordle)

        except ValueError:
            return -1


class TestGetResult(unittest.TestCase):
    """
    Ensure get_result() matches with actual wordle scoring.
    """

    def test_get_result_banal(self):
        """
        Test case data from:
        https://www.reddit.com/r/wordle/comments/ry49ne/illustration_of_what_happens_when_your_guess_has/
        """
        wordle = "banal"

        self.assertEqual(
            get_result("annal", wordle),
            "paccc",
        )
        self.assertEqual(
            get_result("union", wordle),
            "apaaa",
        )
        self.assertEqual(
            get_result("alloy", wordle),
            "ppaaa",
        )

    def test_get_result_click(self):
        """
        Test case data from:
        https://wordfinder.yourdictionary.com/blog/can-letters-repeat-in-wordle-a-closer-look-at-the-rules/
        """
        wordle = "click"
        self.assertEqual(
            get_result("humor", wordle),
            "aaaaa",
        )
        self.assertEqual(
            get_result("dicey", wordle),
            "appaa",
        )
        self.assertEqual(
            get_result("clasp", wordle),
            "ccaaa",
        )
        self.assertEqual(
            get_result("clink", wordle),
            "cccac",
        )
        self.assertEqual(
            get_result("click", wordle),
            "ccccc",
        )

    def test_get_result_elude(self):
        """
        Test case data from:
        https://wordfinder.yourdictionary.com/blog/can-letters-repeat-in-wordle-a-closer-look-at-the-rules/
        """
        wordle = "elude"
        self.assertEqual(
            get_result("crane", wordle),
            "aaaac",
        )
        self.assertEqual(
            get_result("hoist", wordle),
            "aaaaa",
        )
        self.assertEqual(
            get_result("bulky", wordle),
            "appaa",
        )
        self.assertEqual(
            get_result("ledge", wordle),
            "pppac",
        )
        self.assertEqual(
            get_result("elude", wordle),
            "ccccc",
        )

    def test_get_result_close(self):
        """
        Test case data from: https://stackoverflow.com/questions/71324956/wordle-implementation-dealing-with-duplicate-letters-edge-case
        """
        wordle = "close"
        self.assertEqual(
            get_result("cheer", wordle),
            "capaa",
        )
        self.assertEqual(
            get_result("cocks", wordle),
            "cpaap",
        )
        self.assertEqual(
            get_result("leave", wordle),
            "paaac",
        )


def get_result(guess, wordle):
    """
    Simulate the wordle feedback for a guess.
    """
    result = [None] * 5
    wordle_value_counts = pd.Series(list(wordle)).value_counts()
    guess_value_counts = defaultdict(lambda: 0)

    for idx, (guess_, wordle_) in enumerate(zip(guess, wordle)):
        if guess_ == wordle_:
            result[idx] = "c"
            guess_value_counts[guess_] += 1

    for idx, (guess_, wordle_) in enumerate(zip(guess, wordle)):
        if result[idx] is not None:
            continue

        if (
            guess_ in wordle
            and guess_value_counts[guess_] < wordle_value_counts[guess_]
        ):
            result[idx] = "p"
            guess_value_counts[guess_] += 1

        else:
            result[idx] = "a"

    return "".join(result)
