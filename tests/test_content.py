import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from game.loader import load_game_content
from game.validation import validate_content


class ContentTests(unittest.TestCase):
    def setUp(self):
        self.content = load_game_content()

    def test_demo_data_is_consistent(self):
        validate_content(self.content)
        self.assertGreaterEqual(len(self.content.memories), 8)
        self.assertGreaterEqual(len(self.content.questions), 25)
        self.assertGreaterEqual(len(self.content.challenges), 5)

    def test_duplicate_memory_ids_are_rejected(self):
        invalid = copy.deepcopy(self.content)
        invalid.memories[1].id = invalid.memories[0].id
        with self.assertRaisesRegex(ValueError, "Duplicate memory"):
            validate_content(invalid)

    def test_missing_related_memory_is_rejected(self):
        invalid = copy.deepcopy(self.content)
        invalid.questions[0].related_memory_id = "missing"
        with self.assertRaisesRegex(ValueError, "missing memory"):
            validate_content(invalid)

    def test_unmatched_multiple_choice_answer_is_rejected(self):
        invalid = copy.deepcopy(self.content)
        invalid.questions[0].answer = "none of these"
        with self.assertRaisesRegex(ValueError, "one matching option"):
            validate_content(invalid)

    def test_quote_answer_uses_one_of_the_demo_partners(self):
        invalid = copy.deepcopy(self.content)
        quote = next(q for q in invalid.questions if q.category == "who_said_it")
        quote.answer = "not a partner"
        with self.assertRaisesRegex(ValueError, "invalid answer"):
            validate_content(invalid)


if __name__ == "__main__":
    unittest.main()
