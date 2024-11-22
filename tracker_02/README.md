# Tracker_02

This is a demo of a Flask application that uses environment files.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

If your Flask application depends on environment variables in production, it is important to use the same settings during development.

However, instead of resetting your operating system's environment variables each time you run your application (and possibly affecting other projects), you can use the `python-dotenv` module. This module reads environment variables from a `.env` and `.flaskenv` file in your application's directory so Flask can pass them to the application, simulating the desired environment.

> **NOTE** - Using `export` is not recommended because exported variables only persist while the shell is open, and they will affect other projects that use the same settings with different values.

To use the module, install `python-dotenv` in your Python virtual environment and update your `requirements.txt` file:

```shell
python -m pip install python-dotenv
python -m pip freeze > requirements.txt
```

Create two files to store environment variables within your application's root directory (`tracker`):

```shell
touch .env
touch .flaskenv
```

Add any OS-specific environment settings your application uses, like `API_KEY=ABC123`, in the `.env` file.
Add any Flask-specific environment settings your application uses, like `FLASK_RUN_PORT=5000` in the `.flaskenv` file.

When you run your application, Flask will search for those files and use their variables instead of your operating system's actual environment variables.

You can load custom OS environment files when running your application using the `--env-file` option:

```shell
python -B -m flask --env-file .env_alt --app tracker_02 run
```

You can also tell flask to look in the package directory for the `.env` file (`python -B -m flask --env-file tracker_02/.env --app tracker_02 run`).

Here are some guidelines to using environment variable files with Flask:

- Environment variable files store settings that must be set before Flask even starts. We will cover runtime variables and configuration files shortly.
- Do not share the information in environment variable files, like `SECRET_KEY`, on public repositories.

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
|   └── ...
├── tracker_02
|   └── __init__.py
├── __init__.py
├── .env
├── .env_alt
├── .flaskenv
├── hello.py
└── requirements.txt
```

Check the code for issues, then run your application. Do not forget to activate your Python virtual environment first!

```shell
# Check the application for issues
python -B -m pylint tracker_02
# Run the application using environment variables found in `.env` and `.flaskenv`
python -B -m flask --app tracker_02 run
# Run the application using an alternate environment file
python -B -m flask --env-file .env_alt --app tracker_02 run
```

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
