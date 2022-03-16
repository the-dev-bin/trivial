FROM python:3.9-slim

WORKDIR /code

RUN pip install pipenv

COPY . /code

RUN pipenv sync --dev

EXPOSE 8000

CMD [ "pipenv", "run", "devserver" ]
