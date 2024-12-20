# Notes

-----

## tracker_01

- Applied the Flask Package pattern
- Added a module docstring with a **Usage** line
- Added docstrings per PEP 287, reStructuredText Docstring Format
- Added type hints and f-strings
- Added a check to make sure that the minimum Python and Flask requirements were met

```shell
# Install dependencies
python -m pip install flask
python -m pip install pylint
python -m pip freeze > requirements.txt
# Check the application for issues
python -B -m pylint tracker_01
# Run the application without saving bytecode
python -B -m flask --app tracker_01 run
# Run the application in 'hotfix' mode
python -B -m flask --app tracker_01 run --debug
# Run the application on the host IP address (like 192.x.x.x)
# instead of the default address (127.0.0.1)
python -B -m flask --app tracker_01 run --host=0.0.0.0
# Run the application on port 5001 instead of the default port (5000)
python -B -m flask --app tracker_01 run --host=0.0.0.0 --port=5001
```

-----

### tracker_02

- Incorporated project environment variables in local `.env` and `.flaskenv` files
- Protected internal variables within functions by prepending them with an underscore
- Incorporated Jinja2 templating to display variable values in HTML

```shell
# Install dependencies
python -m pip install python-dotenv
python -m pip freeze > requirements.txt
# Check the application for issues
python -B -m pylint tracker_02
# Run the application using environment variables found in `.env` and `.flaskenv`
python -B -m flask --app tracker_02 run
# Run the application using an alternate environment file
python -B -m flask --env-file .env_alt --app tracker_02 run
```

-----

## tracker_03

- Applied the Flask Application Factory pattern
- Incorporated runtime variables found in `config.py`
- Incorporated input validation
- Added `.pylintrc` file to allow Pylint to import package modules and ignore false positives
- Incorporated command line arguments
- Replaced procedural code with functional pattern

```shell
# Check the application for issues
python -B -m pylint tracker_03
# Run the application using the 'default' configuration
python -B -m flask --app tracker_03 run
# Use the 'development' configuration
python -B -m flask --app "tracker_03:create_app(config_name='development')" run
python -B -m flask --app "tracker_03:create_app('development')" run
# Pass a command-line argument
python -B -m flask --app "tracker_03:create_app(foo_var='42')" run
```

-----

## tracker_05

- Added unit testing

```shell
# Check the application for issues
python -B -m pylint tracker_04
# Run the unit tests found in `tests/test_app.py`
python -B -m unittest --buffer --verbose tracker_04/tests/test_app.py
# Run the application
python -B -m flask --app tracker_04 run
```

-----

## tracker_06

- Added unit testing using Coverage.

```shell
# Check the application for issues
python -B -m pylint tracker_04a
# Run the unit tests found in the `tests/` directory using Coverage
coverage run -m unittest discover tracker_04a/tests --verbose --buffer
# See the coverage report in the console
coverage report -m
# See the coverage report in a browser
coverage html --directory tracker_04a/tests/htmlcov
# Run the application
python -B -m flask --app tracker_04a run
```

-----

## tracker_07

- Added profiling.

```shell
# Check the application for issues
python -B -m pylint tracker_05
# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest --verbose --buffer tracker_05/tests/test_app.py
# See the coverage report in the console
coverage report -m
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_05:create_app('profile')" run --without-threads
```

-----

## tracker_08

- Added logging.

```shell
# Check the application for issues
python -B -m pylint tracker_06
# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest discover tracker_06/tests -b -v
# See the coverage report in the console
coverage report -m
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_06:create_app('profile')" run --without-threads
# Create a log when running the Flask application
# python -B -m flask --app "tracker_06:create_app(config_name='development', log_events=True)" run
python -B -m flask --app "tracker_06:create_app('development', True)" run
```

-----

## tracker_09

- Added error handling.

```shell
# Check the application for issues
python -B -m pylint tracker_07
# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest discover tracker_07/tests -b -v
# See the coverage report in the console
coverage report -m
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_07:create_app('profile')" run --without-threads
# Create a log when running the Flask application
# python -B -m flask --app "tracker_07:create_app(config_name='development', log_events=True)" run
python -B -m flask --app "tracker_07:create_app('development', True)" run
```

-----

## tracker_10

- Add templates.

-----

## tracker_11

- Added database.

-----

## tracker_12

- Added blueprints.

-----

## tracker_13

- Added API

-----

## List of Commands

```shell
python3.12 venv $PWD/.venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install flask
python -m pip install pylint
python -m pip install python-dotenv
python -m pip install coverage
python -m pip install Flask-SQLAlchemy
python -m pip install Flask-Migrate
python -m pip install flask-wtf
python -m pip install flask-login
python -m pip freeze > requirements.txt
```
