# Tracker v04a

This is a sub-demo of a Flask application that incorporates Coverage, a tool for measuring code coverage of Python programs.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Unit tests the Flask application using coverage and the unit tests found in `tests/test_app.py`:

- `coverage run -m unittest --verbose --buffer tracker_04a/tests/test_app.py`
- `coverage report -m`
- `coverage html --directory tracker_04a/tests/htmlcov`

-----

## Notes

From the documentation at <https://coverage.readthedocs.io/en/latest/>:

*Coverage.py is a tool for measuring code coverage of Python programs. It monitors your program, noting which parts of the code have been executed, then analyzes the source to identify code that could have been executed but was not.*

*Coverage measurement is typically used to gauge the effectiveness of tests. It can show which parts of your code are being exercised by tests, and which are not.*

Install Coverage:

```shell
python -m pip install coverage
coverage --version
python -m pip freeze > requirements.txt
```

Your application structure should be like the following:

```text
tracker
├── tracker_01
├── ...
├── tracker_04a
|   ├── tests
|   |   ├── __init__.py
|   |   └── test_app.py
|   ├── __init__.py
|   └── config.py
├── venv
|   └── ...
├── .coverage
├── .env
├── .flaskenv
├── .gitignore
├── hello.py
└── requirements.txt
```

Review the code and run your application. Do not forget to activate your Python virtual environment first!

> **NOTE** - Coverage will create a `__pycache__` folder. You may delete this folder when you are done.

- `coverage run -m unittest --verbose --buffer tracker_04a/tests/test_app.py`
- `coverage report -m`

```text
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
tracker_04a\__init__.py            42      2    95%   62-63
tracker_04a\config.py               6      0   100%
tracker_04a\tests\__init__.py       0      0   100%
tracker_04a\tests\test_app.py      74      9    88%   69-70, 81-82, 94-95, 102-103, 139
-------------------------------------------------------------
TOTAL                             122     11    91%
```

If you look at the lines that Coverage says are not covered, they are the `except` part of a `try-except` block. Coverage does not measure code coverage for exceptions unless they are actually raised during test execution. Since you cannot raise those exceptions without adding bad code to your application, accept and explain the lack of coverage in any code quality report you must maintain or submit.

To see the results in a browser, run the following command:

```shell
coverage html --directory tracker_04a/tests/htmlcov
```

Coverage will create and populate the `tracker_04a/tests/htmlcov` directory with a web page. Open a browswer and navigate to <tracker/tracker_04a/tests/htmlcov/index.html> to see the web page.

When you are finished, move on to the next version.
