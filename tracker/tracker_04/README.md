# Tracker v04

This is a demo of a Flask application that incorporates unit testing.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Runs the Flask application or unit tests found in `tests/test_app.py`:

- `python -B -m flask --app tracker_04 run`
- `python -B -m unittest --verbose --buffer tracker_04/tests/test_app.py`

-----

## Notes

Testing your application

Your application structure should be like the following:

```text
tracker
├── tracker_01
├── ...
├── tracker_04
|   ├── tests
|   |   ├── __init__.py
|   |   └── test_app.py
|   ├── __init__.py
|   └── config.py
├── venv
|   └── ...
├── .env
├── .flaskenv
├── .gitignore
├── hello.py
└── requirements.txt
```

Review the code and run your application. Do not forget to activate your Python virtual environment first!

> **NOTE** - Enclose options in quotation marks when using special characters.

- `python -B -m flask --app tracker_04 run`
- `python -B -m unittest --verbose --buffer tracker_04/tests/test_app.py`

When you are finished, move on to the next version.
