from collections import defaultdict
from typing import Optional

from trivial import models


class TriviaGame:
    def __init__(self, trivia: models.Trivia):
        self.trivia = trivia
        self.current_question: Optional[models.Question] = None
        self.answers = defaultdict(dict)

    def record_answer(self, sid: str, answer: int):
        assert self.current_question is not None

        self.answers[self.current_question.uid][sid] = answer
