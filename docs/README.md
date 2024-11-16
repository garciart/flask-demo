# Flask Demo

This is a stage-by-stage demonstration of Flask. It allows you to control course assignments using role-based access control (RBAC).

![Assign Users to Course Screenshot](img/assign-users-screenshot.png)

-----

## Roles

- ***Chair:*** Owns the course
- ***Teacher:*** Can administer a course
- ***Student:*** Can view a course

## Administration

Course Administration:

- ***Add a Course:*** Anyone; the creator becomes the Chair of the Course
- ***View Courses:*** Chairs, Teachers, and Students who are assigned to the Courses
- ***View a Course:*** Chairs, Teachers, and Students who are assigned to the Course
- ***Edit a Course:*** Chairs and Teachers who are assigned to the Course
- ***Delete a Course:*** Chairs who are assigned to the Course

Role and User Administration: Administrators only.

-----

## Stages

1. `app` - Default application with all functionality.
2. `v01` - A basic Flask application that uses a package and application factory.
3. `v02` - Unit test a Flask application.
4. `v03` - Use different environment, Flask, and application configuration options.
5. `v04` - Add logging and input validation.
6. `v05` - Use Flask templates.
7. `v06` - Use Flask blueprints.
8. `v07` - Use a SQLite database.
9. `v08` - Use a one-to-many relationship in a database.

-----

## Installing and Running

1. Clone the repository: `git clone https://github/garciart/flask-template`
2. Create a Python virtual environment: `python -m venv venv`
3. Activate the Python virtual environment: `source venv/bin/activate` (Linux) or `venv/Scripts/activate` (Windows)
4. Install pip: `python -m pip install --upgrade pip`
5. Install required packages: `python -m pip install -r requirements.txt`

To run the default application:

- `python -B app.py  # Runs 'app.py', which in turn instantiates and runs the 'app' package`
- `python -B -m flask run  # Flask will look in 'app.py' and in the 'app' directory if the '--app' option is missing`
- `python -B -m flask --app "app" run  # Instantiates and runs the 'app' package`
- `python -B -m flask --app "app" --debug run  # Allow hot reloads`
- `python -B -m flask --app "app" run --host=0.0.0.0  # Allow outside access in NO DEBUG mode`

> **NOTE**
>
> The Python options in the previous commands are (you can also use `python --help` to look up the options):
>
> - `-B`: Don't write `.pyc` files on import; you can also set the option in your environment by using `export PYTHONDONTWRITEBYTECODE=1`
> - `-m mod`: Run library module as a script (terminates the Python option list)
>
> The Flask options in the previous commands are (you can also use `flask --help` to look up the options):
>
> - `-A, --app IMPORT`: The Flask application or factory function to load, in the form 'module:name'. Module can be a dotted import or file path. Name is not required if it is 'app', 'application', 'create_app', or 'make_app', and can be 'name(args)' to pass arguments.
> - `run`: Run a development server. To allow external access to the server (i.e., not `localhost` or `127.0.0.1`), append `--host=0.0.0.0` to the `run` command.
> - `--debug / --no-debug`:  Set debug mode.

To run a specific stage, use a command like:

`python -B -m flask --app "v01" run`

To unit test a specific stage:

`python -B -m unittest --verbose --buffer v02/tests/test_app.py`

To run Tracker using a specific runtime configuration, ensure the class exists in `config.py`, like `TestConfig(Config)`, and include it in the command:

- `python -B -m flask --app "app:create_app(config_class='TestConfig')" run`
- `python -B -m flask --app "v03:create_app(config_class='v03.config.TestConfig')" run`

To run an instance using a specific environment configuration, ensure that:

- You installed `python-dotenv` in your Python virtual environment and you stored any Flask-specific environment settings, like `FLASK_RUN_PORT=5000`, in a local project file like `.flaskenv`.
- You stored any OS-specific environment settings, like `API_KEY=ABC123`, in a local project file like `.env`.

> **NOTE** - Using `export` is not recommended because exported variables only persist while the shell is open and they will affect other projects that use the same setting with different values.

You can then include the environment file in the command:

- `python -B -m flask --app "app" --env-file ".env" run`

Here are some guidelines to using configuration files with Flask:

Use configuration files, like `config.py`:

- To store information and settings that you want to version control and share with other developers.
- To store settings that change the way Flask behaves at runtime, like `LOGGING_LEVEL`.

Use environment files, like `.env` and `.flaskenv`:

- To store information that you do not want to share or version control, like secrets, etc.
- To store settings that must be set before Flask runs, like `FLASK_RUN_PORT`, or settings specific to the operating system on which Flask is running.
- (`.flaskenv`) To set Flask CLI configuration options and development-specific environment variables related to running Flask, like `FLASK_RUN_PORT`.
- (`.env`) To set application-specific environment variables and sensitive information, like `API_KEY`.
- You can reference environment variables in the configuration file so that other developers know the application requires those settings. For example, you can reference a secret key from `.flaskenv` in `config.py` by using `SECRET_KEY=os.environ.get('SECRET_KEY)`
