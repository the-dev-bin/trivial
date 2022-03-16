import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class User:
    name: str
    # TODO: List of str?
    sid: str
    avatar_url: str = None


@dataclass
class Choice:
    id: int
    text: str
    correct: bool


@dataclass
class Question:
    uid: uuid.UUID = field(default_factory=uuid.uuid4, init=False)

    text: str
    notes: Optional[str]
    choices: list[Choice]


@dataclass
class Config:
    pass


@dataclass
class Trivia:
    """A set of trivia challenges"""
    uid: uuid.UUID = field(default_factory=uuid.uuid4, init=False)

    name: str
    owner: User
    config: Config
    challenges: list[Question]
