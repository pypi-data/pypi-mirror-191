FROM opencvcourses/opencv-docker:4.5.1

WORKDIR /home

RUN pip install --no-cache-dir poetry==1.3.2

COPY pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install --no-dev
