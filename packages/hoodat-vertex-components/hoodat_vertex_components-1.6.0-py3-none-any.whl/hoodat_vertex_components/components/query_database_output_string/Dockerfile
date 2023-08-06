FROM python:3.8.13-slim-buster

RUN pip install poetry

COPY pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . .
