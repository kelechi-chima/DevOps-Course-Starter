FROM python:3.9.6-slim-buster

COPY todo_app/ todo_app
COPY .env poetry.toml pyproject.toml wsgi.py ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
EXPOSE 5000
ENTRYPOINT [ "poetry", "run", "gunicorn", "-b 0.0.0.0:5000", "-w 2", "wsgi:app" ]