FROM python:3.9-slim

WORKDIR /code

RUN pip install pipenv

COPY . /code

RUN pipenv sync --dev

CMD [ "pipenv", "run", "devserver" ]
