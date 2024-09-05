"""Starting point for the Blue application.

> **NOTE** - Remember to activate your Python virtual environment before running: `source venv/bin/activate` (Linux) or `venv/Scripts/activate` (Windows).

Blue does not use this file to create the Flask application instance and define routes.

Instead, Blue uses packages contained in subdirectories within the Blue project directory:

blue
├── app
|   ├── __init__.py
|   ├── config.py
|   └── ...
├── v01
├── v02
└── ...

Each package contains an application factory in `__init__.py` that creates the Flask application instance and defines routes. Each package also contains a `config.py` file that allows you to use different settings for testing and debugging.

To run the default `app` package, you would use one of the following commands:

- `python -B -m flask run  # If you do not use the '--app' option, by default, Flask will look for code in 'app.py' or in the 'app' directory`
- `python -B -m flask --app "app" run`
- `python -B -m flask --app "app" run --debug  # Allow hot reloads`
- `python -B -m flask run --host=0.0.0.0  # Allow outside access in NO DEBUG mode`

> **NOTE**
>
> The Python options in the previous commands are:
> -B     : don't write `.pyc` files on import; you can also set the option in your environment by using `export PYTHONDONTWRITEBYTECODE=1`
> -m mod : run library module as a script (terminates the Python option list)

To run a specific version of Blue, use a command like:

`python -B -m flask --app "v01" run`

To run an instance using a specific runtime configuration, ensure the class exists in `config.py`, like `TestConfig(Config)`, and include it in the command:

- `python -B -m flask --app "app:create_app(config_class='TestConfig')" run`
- `python -B -m flask --app "v01:create_app(config_class='v01.config.TestConfig')" run`

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
"""
