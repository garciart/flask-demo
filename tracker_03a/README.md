# Tracker_03a

This is a demo of a Flask application that uses a utility file.

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Keeping all of your code in one file can become difficult to manage and maintain. It can also lead to problems, like accidentally overwriting variables or circular imports. Breaking up your Python code into modules helps you keep your project organized and allows you to reuse code.

In this package, we broke out the `check_system()` function into a separate helper file named `app_utils.py`. We also created a separate function named `validate_inputs()`, which we will use often to ensure arguments are of the correct type and that they are not empty, if required.

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_03a
|   ├── __init__.py
|   ├── app_utils.py
|   └── config.py
├── .env
├── .env_alt
├── .flaskenv
├── .pylintrc
├── __init__.py
├── hello.py
└── requirements.txt
```

Review the code and run your application. Do not forget to activate your Python virtual environment first!

> **NOTE** - Enclose options in quotation marks when using special characters.

```shell
# Check the application for errors
python -B -m pylint tracker_03a
# Run the application using the 'default' configuration
python -B -m flask --app tracker_03a run
```

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
