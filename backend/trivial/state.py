from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

from trivial import models


class LiveQuestion:
    def __init__(self, question: models.Question):
        self.question = question
        self.start = datetime.now()

    @property
    def uid(self):
        return self.question.uid


class TriviaGame:
    def __init__(self, game_id: str, trivia: models.Trivia):
        self.game_id = game_id
        self.trivia = trivia
        self._questions_iter = iter(trivia.questions)
        self.current_question: Optional[LiveQuestion] = None
        self.answers = defaultdict(dict)

    @property
    def owner(self):
        return self.trivia.owner

    def record_answer(self, sid: str, answer: int):
        assert self.current_question is not None

        if self.trivia.config.timer and datetime.now() < self.current_question.start + timedelta(seconds=self.trivia.config.timer):
            self.answers[self.current_question.uid][sid] = answer

    def get_scores(self) -> dict[str, int]:
        score = {}
        for question in self.trivia.questions:
            for sid, answer in self.answers[question.uid].items():
                if question.choices[answer].correct:
                    score[sid] = score.setdefault(sid, 0) + 1

        return score

    def advance_question(self):
        question = next(self._questions_iter, None)
        if question:
            self.current_question = LiveQuestion(question)
        else:
            self.current_question = None
