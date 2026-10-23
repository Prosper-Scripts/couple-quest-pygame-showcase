"""Pure timeline rules, independent of rendering and random selection."""

from datetime import date

from game.models import Memory


def chronology_key(memory: Memory) -> tuple[date, str]:
    """Sort by an ISO date, falling back to January 1 for year-only memories.

    A populated date must be ISO 8601 (YYYY-MM-DD), and must agree with the
    event's year. This keeps the timeline answer independent of JSON file order.
    """
    if memory.date:
        try:
            event_date = date.fromisoformat(memory.date)
        except ValueError as exc:
            raise ValueError(
                f"Memory '{memory.id}' must use an ISO date (YYYY-MM-DD)."
            ) from exc
        if event_date.year != memory.year:
            raise ValueError(f"Memory '{memory.id}' has a date/year mismatch.")
    else:
        event_date = date(memory.year, 1, 1)

    return event_date, memory.id


def chronological_memories(memories: list[Memory]) -> list[Memory]:
    """Return a new list of events from earliest to latest."""
    return sorted(memories, key=chronology_key)
