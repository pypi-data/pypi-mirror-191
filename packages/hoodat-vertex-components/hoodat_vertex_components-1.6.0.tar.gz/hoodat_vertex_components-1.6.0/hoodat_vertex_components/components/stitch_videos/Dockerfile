FROM python:3.8.13-slim-buster

# Install system dependencies
RUN apt -y update && apt -y install ffmpeg

# Install python dependencies
RUN pip install poetry
COPY pyproject.toml poetry.lock /
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy sample data into container
COPY sample sample
