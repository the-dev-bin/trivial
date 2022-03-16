FROM python:3.9-slim

WORKDIR /code

RUN pip install pipenv

COPY . /code

RUN pipenv --rm
RUN pipenv sync --dev
RUN pipenv run pip freeze

RUN pipenv run devserver
