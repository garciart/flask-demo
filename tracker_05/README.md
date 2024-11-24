# Tracker_05

This is a demo of a Flask application that incorporates unit testing.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

The application factory pattern allows you to organize your code into functions. Functions and methods allow you to consolidate related code, like system checks, into small, manageable, and reusable blocks. Using functions and methods also reduces code repetition, which reduces complexity and improves maintainability. Additionally, functions and methods can be *unit-tested* effectively.

A unit test is a small, automated test that focuses on testing a single unit of functionality in isolation, such as a function or method.

After you refactor a function or method, you can run unit tests to ensure that it still behaves as expected, by checking that the function or method correctly handles both valid inputs and edge cases (invalid inputs) while producing the correct output.

Without unit tests, you may unknowingly introduce bugs when you edit your code, especially as your application gets larger, because refactoring might change something subtle that impacts other parts of the program. This is called **regression**, since the code *regressed* to a point where it no longer works. With unit tests in place, you can confirm that everything still works correctly before deploying your changes.

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_05
|   ├── tests
|   |   ├── __init__.py
|   |   ├── test_app.py
|   |   └── test_app_utils.py
|   ├── __init__.py
|   ├── app_utils.py
|   └── config.py
├── __init__.py
├── .env
├── .env_alt
├── .flaskenv
├── .pylintrc
├── hello.py
└── requirements.txt
```

Run the unit tests to make sure that your changes did not regress the code:

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
# python -B -m unittest discover tracker_05/tests --buffer --verbose
python -B -m unittest discover tracker_05/tests -b -v
```

Check the code for issues, then run your application. Do not forget to activate your Python virtual environment first!

```shell
# Check the application for issues
python -B -m pylint tracker_05
# Run the application using the 'default' configuration
python -B -m flask --app tracker_05 run
```

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
