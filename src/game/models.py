from dataclasses import dataclass, field


@dataclass
class CoupleProfile:
    title: str
    partner_one: str
    partner_two: str
    years_together: int
    tagline: str
    anniversary: str
    home_message: str


@dataclass
class Memory:
    id: str
    title: str
    year: int
    location: str
    description: str
    date: str | None = None
    tags: list[str] = field(default_factory=list)
    photo: str | None = None


@dataclass
class Question:
    id: str
    category: str
    prompt: str
    answer: str | None = None
    options: list[str] = field(default_factory=list)
    related_memory_id: str | None = None


@dataclass
class Challenge:
    id: str
    title: str
    prompt: str
    reward_text: str


@dataclass
class GameContent:
    profile: CoupleProfile
    memories: list[Memory]
    questions: list[Question]
    challenges: list[Challenge]
