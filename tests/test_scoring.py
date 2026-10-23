import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from game.scoring import grade_memory_answer


class ScoringTests(unittest.TestCase):
    def test_matching_answer_ignores_case_and_outer_whitespace(self):
        self.assertTrue(grade_memory_answer("  HARBOR BOOKSHOP ", "Harbor Bookshop"))

    def test_incorrect_answer_does_not_pass(self):
        self.assertFalse(grade_memory_answer("Willow Square", "Harbor Bookshop"))


if __name__ == "__main__":
    unittest.main()
