# Tracker_04a

This is a demo of a Flask application that incorporates Coverage, a tool for measuring code coverage of Python programs.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

Instead of using the `unittest` module, we will use Coverage to unit test our code. Not only does Coverage test, but it also locates code that is not covered by a unit test. From the documentation at <https://coverage.readthedocs.io/en/latest/>:

*Coverage.py is a tool for measuring code coverage of Python programs. It monitors your program, noting which parts of the code have been executed, then analyzes the source to identify code that could have been executed but was not.*

*Coverage measurement is typically used to gauge the effectiveness of tests. It can show which parts of your code are being exercised by tests, and which are not.*

Install Coverage:

```shell
python -m pip install coverage
coverage --version
python -m pip freeze > requirements.txt
```

Since you will not test the unit tests themselves, tell Coverage to ignore your `tests` directory by adding a `.coveragerc` file with the following code:

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
|   |   ├── test_app.py
|   |   └── test_app_utils.py
|   ├── __init__.py
|   ├── app_utils.py
|   └── config.py
├── __init__.py
├── .coverage
├── .coveragerc
├── .env
├── .env_alt
├── .flaskenv
├── .pylintrc
├── hello.py
└── requirements.txt
```

Run Coverage to make sure that your changes did not regress the code:

> **NOTES:**
>
> - Test from the project directory (e.g., `flask-demo`, not `tracker_XX`)
> - Do not log events when unit testing or each test will create a log file.
> - Using `--buffer` and `--verbose` together provides a good balance of output,
>   since `--buffer` hides console output from the application
>   and `--verbose` displays the test's docstring
>   (ex., `Test that check_system() fails because min_python_version is not type float ... ok`)

```shell
# Run the unit tests found in the `tests` directory
# coverage -m unittest discover tracker_04a/tests --buffer --verbose
coverage run -m unittest discover tracker_04a/tests -b -v
```

> **NOTE** - Coverage will create a `__pycache__` folder. Delete it when you are done testing.

Once the tests are complete, look at the results:

```shell
coverage report -m
```

**Output:**

```text
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
tracker_04a\__init__.py       26      2    92%   67-68
tracker_04a\app_utils.py      24      0   100%
tracker_04a\config.py          6      0   100%
--------------------------------------------------------
TOTAL                         56      2    96%
```

If you look at the lines that Coverage says are not covered, they are the `except` part of a `try-except` block. Coverage does not measure code coverage for exceptions unless they are actually raised during test execution. Since you cannot raise those exceptions without adding bad code to your application, use the `# pragma: no cover` comment to skip checking the line of code.

To see the results in a browser, run the following command:

```shell
coverage html --directory tracker_04a/tests/htmlcov
```

Coverage will create and populate the `tracker_04a/tests/htmlcov` directory with a web page. Open a browser and navigate to <tracker_04a/tests/htmlcov/index.html> to see the web page.

Check the code for issues, then run your application. Do not forget to activate your Python virtual environment first!

```shell
# Check the application for issues
python -B -m pylint tracker_04
# Run the application using the 'default' configuration
python -B -m flask --app tracker_04 run
```

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
