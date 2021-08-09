FROM python:3.9.6-slim-buster as base

COPY .env poetry.toml pyproject.toml wsgi.py ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
COPY todo_app/ todo_app
EXPOSE 5000

FROM base as development
ENV FLASK_ENV=development
ENTRYPOINT [ "poetry", "run", "flask", "run", "--host=0.0.0.0" ]

FROM base as production
ENTRYPOINT [ "poetry", "run", "gunicorn", "-b 0.0.0.0:5000", "-w 2", "wsgi:app" ]