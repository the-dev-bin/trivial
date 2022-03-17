from collections import defaultdict
from typing import Optional

from trivial import models


class TriviaGame:
    def __init__(self, game_id: str, trivia: models.Trivia):
        self.game_id = game_id
        self.trivia = trivia
        self._questions_iter = iter(trivia.questions)
        self.current_question: Optional[models.Question] = None
        self.answers = defaultdict(dict)

    @property
    def owner(self):
        return self.trivia.owner

    def record_answer(self, sid: str, answer: int):
        assert self.current_question is not None

        self.answers[self.current_question.uid][sid] = answer

    def advance_question(self):
        self.current_question = next(self._questions_iter, None)
