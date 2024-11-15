# Tracker_02

This is a demo of a Flask application that uses environment files.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Runs the Flask application using environment variables found in `tracker/.env` and `tracker/.flaskenv`:

- `python -B -m flask --app tracker_02 run`

-----

## Notes

If your Flask application depends on environment variables in production, it is important to identify them and to use them during development.

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

While you can place the `.flaskenv` file in the package's directory (`tracker/tracker_02/.flaskenv`), the `.env` must be in the application's root directory (`tracker/.env`).

> **NOTE** - You can also load custom OS environment files when running your application using the `--env-file` option:
>
> ```shell
> python -B -m flask --app tracker_02 run --env-file .alt_env run
> ```
>
> However, `.env` always take precedence, and Flask will not load the alternate environment file if a `.env` file exists in the same directory.

Here are some guidelines to using environment variable files with Flask:

- Environment variable files store settings that must be set before Flask even starts. We will cover runtime variables and configuration files shortly.
- Do not share the information in environment variable files, like `SECRET_KEY`, on public repositories.

Your application structure should be like the following:

```text
tracker
├── tracker_01
|   └── ...
├── tracker_02
|   └── __init__.py
├── venv
|   └── ...
├── .env
├── .flaskenv
├── hello.py
└── requirements.txt
```

Review the code and run your application. Do not forget to activate your Python virtual environment first!

- `python -B -m flask --app tracker_02 run`

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
