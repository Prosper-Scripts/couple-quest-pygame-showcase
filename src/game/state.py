from dataclasses import dataclass, field
import random

from game.models import GameContent, Memory, Question
from game.timeline import chronological_memories


@dataclass
class GameState:
    content: GameContent
    hearts: int = 3
    score: int = 0
    current_mode: str = "memory_lane"
    current_question_index: int = 0
    session_questions: list[Question] = field(default_factory=list)
    session_memories: list[Memory] = field(default_factory=list)
    session_summary: list[str] = field(default_factory=list)
    active_challenge_index: int = 0
    audio: object | None = None
    feedback_message: str = ""
    feedback_color: tuple[int, int, int] = (72, 43, 35)
    feedback_timer: float = 0.0

    def reset_mode(self, mode_name: str) -> None:
        self.current_mode = mode_name
        self.score = 0
        self.hearts = 3
        self.current_question_index = 0
        self.session_questions = []
        self.session_memories = []
        self.session_summary = []
        self.active_challenge_index = 0
        self.feedback_message = ""
        self.feedback_timer = 0.0

        category_map = {
            "memory_lane": {"memory_lane"},
            "who_said_it": {"who_said_it"},
            "heart_talk": {"deep_talk", "marriage_talk", "couple_goals"},
        }

        selected_categories = category_map.get(mode_name, set())
        pool = [q for q in self.content.questions if q.category in selected_categories]
        random.shuffle(pool)

        if mode_name == "memory_lane":
            self.session_questions = pool[: min(7, len(pool))]
        elif mode_name == "who_said_it":
            self.session_questions = pool[: min(6, len(pool))]
        elif mode_name == "heart_talk":
            self.session_questions = pool[: min(8, len(pool))]
        elif mode_name == "timeline":
            sample_size = min(4, len(self.content.memories))
            sampled = random.sample(self.content.memories, sample_size)
            self.session_memories = chronological_memories(sampled)

        if mode_name == "love_missions" and self.content.challenges:
            self.active_challenge_index = random.randrange(len(self.content.challenges))

    def add_result(self, text: str) -> None:
        self.session_summary.append(text)

    def active_question(self) -> Question | None:
        if 0 <= self.current_question_index < len(self.session_questions):
            return self.session_questions[self.current_question_index]
        return None

    def active_timeline_memory(self) -> Memory | None:
        if 0 <= self.current_question_index < len(self.session_memories):
            return self.session_memories[self.current_question_index]
        return None

    def remaining_timeline_memories(self) -> list[Memory]:
        """Only unsolved events should remain available as timeline options."""
        return self.session_memories[self.current_question_index:]

    def set_feedback(self, message: str, color: tuple[int, int, int], duration: float = 1.2) -> None:
        self.feedback_message = message
        self.feedback_color = color
        self.feedback_timer = duration

    def update(self, dt: float) -> None:
        if self.feedback_timer > 0:
            self.feedback_timer = max(0.0, self.feedback_timer - dt)
            if self.feedback_timer == 0:
                self.feedback_message = ""
