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

The application factory pattern allows you to organize your code into functions. Functions and methods allow you to consolidate related code, like system checks, into small, manageable, and reusable blocks. Using functions and methods also reduces code repetition, which reduces complexity and improves maintainability. Additionally, functions and methods can be *unit-tested* effectively.

A unit test is a small, automated test that focuses on testing a single unit of functionality in isolation, such as a function or method.

After you refactor a function or method, you can run unit tests to ensure that it still behaves as expected, by checking that the function or method correctly handles both valid inputs and edge cases (invalid inputs) while producing the correct output.

Without unit tests, you may unknowingly introduce bugs when you edit your code, especially as your application gets larger, because refactoring might change something subtle that impacts other parts of the program. This is called **regression**, since the code *regressed* to a point where it no longer works. With unit tests in place, you can confirm that everything still works correctly before deploying your changes.

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
