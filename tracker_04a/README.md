# Tracker_04a

This is a demo of a Flask application that incorporates Coverage, a tool for measuring code coverage of Python programs.

BROKE UP UNIT TESTS! COMMAND TO RUN IS `coverage run -m unittest --verbose --buffer tracker_04a/tests/test_*.py`

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

```shell
# Check the application for errors
python -B -m pylint tracker_04a
# Run the unit tests found in `tests/test_app.py` using Coverage
coverage run -m unittest --verbose --buffer tracker_04a/tests/test_app.py
# See the coverage report in the console
coverage report -m
# See the coverage report in a browser
coverage html --directory tracker_04a/tests/htmlcov
# Run the application
python -B -m flask --app tracker_04a run
```

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

You will not write tests to test your unit tests, so tell Coverage to ignore your `tests` directory by adding a `.coveragerc` file with the following code:

```ini
[run]
omit = */tests/*
```

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_04a
|   ├── tests
|   |   ├── __init__.py
|   |   └── test_app.py
|   ├── __init__.py
|   └── config.py
├── .coverage
├── .coveragerc
├── .env
├── .env_alt
├── .flaskenv
├── __init__.py
├── hello.py
└── requirements.txt
```

Review the code and run your application. Do not forget to activate your Python virtual environment first!

```shell
echo 'default' | python -B -m unittest --buffer --verbose tracker_04a/tests/test_app.py
python -B -m flask --app tracker_04a run
```

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>.

Now, run Coverage in interactive mode. When prompted, enter "development" or press <kbd>Enter</kbd> to accept the **default** configuration:

> **NOTE** - The reason I added user interaction to `test_app.py` is because you cannot pass arguments, like `--config development`, to `test_app.py` using `sys.argv` or the `argparse` module; the `unittest` module will read them instead.

```shell
coverage run -m unittest --buffer --verbose tracker_04a/tests/test_app.py
```

To run Coverage without user interaction, pipe the desired configuration into the command as input:

```shell
echo 'default' | coverage run -m unittest --buffer --verbose tracker_04a/tests/test_app.py
```

> **NOTE** - Coverage will create a `__pycache__` folder. You may delete this folder when you are done.

Once the tests are complete, look at the results:

```shell
coverage report -m
```

**Output:**

```text
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
tracker_04a\__init__.py            42      2    95%   67-68
tracker_04a\config.py               6      0   100%
-------------------------------------------------------------
TOTAL                              48      2    96%
```

If you look at the lines that Coverage says are not covered, they are the `except` part of a `try-except` block. Coverage does not measure code coverage for exceptions unless they are actually raised during test execution. Since you cannot raise those exceptions without adding bad code to your application, use the `# pragma: no cover` comment to skip checking the line of code.

To see the results in a browser, run the following command:

```shell
coverage html --directory tracker_04a/tests/htmlcov
```

Coverage will create and populate the `tracker_04a/tests/htmlcov` directory with a web page. Open a browser and navigate to <tracker_04a/tests/htmlcov/index.html> to see the web page.

When you are finished, move on to the next version.
