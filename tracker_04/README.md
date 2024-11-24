# Tracker_04

This is a demo of a Flask application that uses a utility file.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

Keeping all of your code in one file can become difficult to manage and maintain. It can also lead to problems, like accidentally overwriting variables or circular imports. Breaking up your Python code into modules helps you keep your project organized and allows you to reuse code.

In this package, we broke out the `check_system()` function into a separate helper file named `app_utils.py`. We also created a separate function named `validate_inputs()`, which we will use often to ensure arguments of other functions and methods are of the correct type and are not empty.

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_04
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

Check the code for issues, then run your application. Do not forget to activate your Python virtual environment first!

```shell
# Check the application for issues
python -B -m pylint tracker_04
# Run the application using the 'default' configuration
python -B -m flask --app tracker_04 run
```

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
