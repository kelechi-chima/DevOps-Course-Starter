# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Environment variables
The app reads TRELLO_API_KEY and TRELLO_API_TOKEN from the .env file. You will need to register on Trello to get your API key and token.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running tests

### Unit tests
The unit tests are run with pytest. From a terminal you can run one of the following:
```bash
 * poetry run pytest
 * python -m pytest
```

To run all tests in a module (e.g test_view_model.py) run the following from the root directory:
```bash
 pytest tests/test_view_model.py
```

To run a single test in a module (e.g test_view_model.py) run the following from the root directory:
```bash
 pytest tests/test_view_model.py::test_returns_only_todo_items
```

All tests or individual tests can also be run from an IDE. If using Visual Studio Code you can follow the guide at https://code.visualstudio.com/docs/python/testing.

### Integration tests

The integration tests are under tests_e2e. From a terminal you can run them as follows:
```bash
 * poetry run pytest tests_e2e
 * python -m pytest tests_e2e
```

### Setting up Chrome Driver
https://chromedriver.chromium.org/getting-started

If you get an error from Mac OS that the chrome driver cannot be executed please read the workaround here: https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de

## Running application with Docker 
The Dockerfile supports multi-stage builds (development and production). In both stages the .env file containing application secrets are not copied into the image. Instead it has to be passed with the --env-file option to docker run.

### Development
The development stage builds an image that can be used to run the app with Flask in a container. 
```bash
 * docker build -t todo-app --target=development .
 * docker run --rm -p 5000:5000 --env-file ./.env --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app --name todo-app todo-app
```

You can also use docker-compose to create and start the development container with docker-compose up. You can use the --build option to make sure that it rebuilds the image if necessary.

### Production
The production stage builds an image that can be used to run the app with Gunicorn + Flask in a container.
```bash
 * docker build -t todo-app --target=production .
 * docker run --rm -p 5000:5000 --env-file ./.env --name todo-app todo-app
```