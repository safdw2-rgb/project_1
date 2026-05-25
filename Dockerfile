FROM python:3.14

ENV APP_HOME=/app

WORKDIR $APP_HOME

RUN pip install poetry

COPY pyproject.toml poetry.lock* $APP_HOME/

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . $APP_HOME

ENTRYPOINT ["python", "main.py"]