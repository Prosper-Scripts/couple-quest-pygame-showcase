"""Content consistency checks that do not depend on Pygame."""

from game.models import GameContent
from game.timeline import chronology_key


SUPPORTED_CATEGORIES = {
    "memory_lane", "who_said_it", "deep_talk", "couple_goals", "marriage_talk"
}


def validate_content(content: GameContent) -> None:
    """Raise ValueError with a useful message for invalid demo data."""
    if content.profile.partner_one == content.profile.partner_two:
        raise ValueError("Partner names must be distinct.")

    for label, items in (
        ("memory", content.memories),
        ("question", content.questions),
        ("challenge", content.challenges),
    ):
        ids = [item.id for item in items]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate {label} ID found.")

    memory_ids = {memory.id for memory in content.memories}
    for memory in content.memories:
        chronology_key(memory)

    for question in content.questions:
        if question.category not in SUPPORTED_CATEGORIES:
            raise ValueError(f"Question '{question.id}' has an unknown category.")
        if question.related_memory_id and question.related_memory_id not in memory_ids:
            raise ValueError(f"Question '{question.id}' references a missing memory.")
        if question.category == "memory_lane":
            if not question.answer or len(question.options) < 2:
                raise ValueError(f"Memory question '{question.id}' needs an answer and options.")
            if sum(option.casefold().strip() == question.answer.casefold().strip()
                   for option in question.options) != 1:
                raise ValueError(f"Memory question '{question.id}' needs exactly one matching option.")
        elif question.category == "who_said_it":
            if question.answer not in (content.profile.partner_one, content.profile.partner_two):
                raise ValueError(f"Quote question '{question.id}' has an invalid answer.")
