import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from game.loader import load_game_content
from game.state import GameState


class StateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = load_game_content()

    def test_timeline_selection_is_chronological(self):
        random.seed(100)
        state = GameState(self.content)
        state.reset_mode("timeline")
        self.assertEqual(len(state.session_memories), 4)
        dates = [memory.date for memory in state.session_memories]
        self.assertEqual(dates, sorted(dates))

    def test_completed_timeline_choices_disappear(self):
        state = GameState(self.content)
        state.reset_mode("timeline")
        first = state.active_timeline_memory()
        self.assertEqual(len(state.remaining_timeline_memories()), 4)
        state.current_question_index += 1
        self.assertNotIn(first, state.remaining_timeline_memories())
        self.assertEqual(len(state.remaining_timeline_memories()), 3)

    def test_mode_pools_and_limits(self):
        state = GameState(self.content)
        for mode, expected_categories, limit in (
            ("memory_lane", {"memory_lane"}, 7),
            ("who_said_it", {"who_said_it"}, 6),
            ("heart_talk", {"deep_talk", "marriage_talk", "couple_goals"}, 8),
        ):
            with self.subTest(mode=mode):
                state.reset_mode(mode)
                self.assertEqual(len(state.session_questions), limit)
                self.assertTrue(all(q.category in expected_categories for q in state.session_questions))

    def test_reset_clears_previous_round(self):
        state = GameState(self.content)
        state.score = 6
        state.hearts = 0
        state.session_summary.append("Old message")
        state.set_feedback("Old feedback", (1, 2, 3))
        state.reset_mode("love_missions")
        self.assertEqual((state.score, state.hearts), (0, 3))
        self.assertEqual(state.session_summary, [])
        self.assertEqual(state.feedback_message, "")
        self.assertEqual(state.feedback_timer, 0.0)
        self.assertLess(state.active_challenge_index, len(self.content.challenges))

    def test_empty_timeline(self):
        from game.models import GameContent
        empty = GameContent(self.content.profile, [], [], [])
        state = GameState(empty)
        state.reset_mode("timeline")
        self.assertIsNone(state.active_timeline_memory())
        self.assertEqual(state.remaining_timeline_memories(), [])


if __name__ == "__main__":
    unittest.main()
