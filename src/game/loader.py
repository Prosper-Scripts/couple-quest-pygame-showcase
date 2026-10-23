import json

from config import DATA_DIR
from game.models import Challenge, CoupleProfile, GameContent, Memory, Question
from game.validation import validate_content


def _read_json(filename: str) -> list[dict] | dict:
    with (DATA_DIR / filename).open("r", encoding="utf-8") as file:
        return json.load(file)


def load_game_content() -> GameContent:
    profile_data = _read_json("couple_profile.json")
    memories_data = _read_json("memories.json")
    questions_data = _read_json("questions.json")
    challenges_data = _read_json("challenges.json")

    profile = CoupleProfile(**profile_data)
    memories = [Memory(**memory) for memory in memories_data]
    questions = [Question(**question) for question in questions_data]
    challenges = [Challenge(**challenge) for challenge in challenges_data]

    content = GameContent(
        profile=profile,
        memories=memories,
        questions=questions,
        challenges=challenges,
    )
    validate_content(content)
    return content

