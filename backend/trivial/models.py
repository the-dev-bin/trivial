import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class User:
    uid: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)

    name: str
    # TODO: List of str?
    sid: str
    avatar_url: Optional[str] = None

    def asdict(self):
        return {
            "uid": self.name,
            "name": self.name,
            "avatar_url": self.avatar_url
        }


@dataclass
class Choice:
    id: int
    text: str
    correct: bool


@dataclass
class Question:
    uid: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)

    text: str
    notes: Optional[str]
    choices: list[Choice]


@dataclass
class Config:
    show_players: bool = True
    # In seconds
    timer: Optional[float] = 30


@dataclass
class Trivia:
    """A set of trivia questions"""
    uid: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)

    name: str
    owner: User
    config: Config
    questions: list[Question]
