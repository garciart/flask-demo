# Tracker_03

This is a demo of a Flask application that uses an application factory and a configuration file.

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

The Application Factory pattern allows you to use different runtime configurations without having to modify the application's code. For example, instead of creating separate versions of the application for debugging, testing, and production (which increasing maintenance), you can modify the `create_app` method to accept configuration settings, like `logging_level`. You can then pass the settings to the application at runtime, like `create_app(logging_level=logging.DEBUG)` when debugging.

However, your runtime configurations may have a lot of settings, like database locations, server addresses, etc. To avoid long command lines, you can organize these settings into separate classes within a `config.py` file. Then, you would then modify the `create_app` method to accept a configuration *name*, like `development`, and pass it to the application at runtime, like `create_app(config_name=development)` when debugging. This way, you can easily switch between configurations without changing the application code.

Another advantage of using an application factory is that you can add additional command-line arguments other than `config_name`:

```python
def create_app(config_name: str = 'default', foo_var: str = 'bar') -> flask.Flask:
```

- If you run `python -B -m flask --app tracker_03 run`, `foo_var` will equal `bar`.
- If you run `python -B -m flask --app "tracker_03:create_app(foo_var='42')" run`, `foo_var` will equal `42`.

One more thing: When you check your package for errors, Pylint may return `tracker_03/__init__.py:30:0: E0401: Unable to import 'tracker_03.config' (import-error)`. This occurs because, when Pylint looks at `PYTHONPATH`, it cannot find your project directory and, therefore, cannot import modules from it. Unfortunately, the best option, setting `PYTHONPATH` in your `.env`, does not work, and running `export PYTHONPATH=$(pwd)` may break other applications. The solution is to create a `.pylintrc` file with the following code:

```ini
# code: language=ini
# Settings for Pylint
[MAIN]
init-hook='import sys; sys.path.append('.')'
```
 
Using `init-hook` and `.` will tell Pylint to look in the current directory, which should be your project directory, for modules to import.

You may also want to disable the `too-few-public-methods` message in `.pylintrc`, since the configuration classes in `config.py` will not need public methods:

```ini
[MESSAGES CONTROL]
disable=too-few-public-methods
```

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_03
|   ├── __init__.py
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
python -B -m pylint tracker_03
# Run the application using the configuration variables found in `config.py`
python -B -m flask --app "tracker_03:create_app(config_name='development')" run
python -B -m flask --app "tracker_03:create_app('development')" run
# Run the application using the 'default' configuration
python -B -m flask --app tracker_03 run
# Run the application with a value for the 'foo_var' argument
python -B -m flask --app "tracker_03:create_app(foo_var='42')" run
```

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
