FROM python:3.8.13-slim-buster

RUN apt-get -y update && apt-get -y install git
RUN apt -y update && apt -y install ffmpeg
RUN pip install poetry

COPY pyproject.toml poetry.lock /

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY friends.mp4 /
