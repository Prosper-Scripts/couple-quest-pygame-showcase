import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from game.models import Memory
from game.timeline import chronological_memories, chronology_key


def memory(identifier, year, event_date):
    return Memory(identifier, identifier, year, "Test Place", "Description", event_date)


class TimelineTests(unittest.TestCase):
    def test_chronology_ignores_source_file_order(self):
        events = [
            memory("latest", 2025, "2025-12-20"),
            memory("earliest", 2021, "2021-03-03"),
            memory("middle", 2023, "2023-11-11"),
        ]
        self.assertEqual([m.id for m in chronological_memories(events)],
                         ["earliest", "middle", "latest"])
        self.assertEqual(events[0].id, "latest", "Input order must not be mutated")

    def test_ordering_same_year_uses_exact_date(self):
        events = [memory("later", 2022, "2022-10-01"), memory("earlier", 2022, "2022-01-31")]
        self.assertEqual([m.id for m in chronological_memories(events)], ["earlier", "later"])

    def test_year_only_fallback(self):
        self.assertEqual(chronology_key(memory("one", 2020, None))[0].isoformat(), "2020-01-01")

    def test_rejects_non_iso_dates(self):
        with self.assertRaisesRegex(ValueError, "ISO date"):
            chronology_key(memory("one", 2021, "April 10, 2021"))

    def test_rejects_year_mismatch(self):
        with self.assertRaisesRegex(ValueError, "mismatch"):
            chronology_key(memory("one", 2021, "2022-01-01"))


if __name__ == "__main__":
    unittest.main()
