from dataclasses import dataclass
from typing import List


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
    text: str
    notes: str
    choices: list[Choice]


@dataclass
class Config:
    pass


@dataclass
class Trivia:
    """A set of trivia challenges"""
    name: str
    owner: User
    config: Config
    challenges: List[Question]
