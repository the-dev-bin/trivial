from dataclasses import dataclass
from typing import List


@dataclass
class User:
    name: str
    # TODO: List of str?
    sid: str
    api_key: str


@dataclass
class Challenge:
    pass


@dataclass
class Trivia:
    """A set of trivia challenges"""
    name: str
    owner: User
    challenges: List[Challenge]
