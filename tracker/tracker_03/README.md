# Tracker v03

This is a demo of a Flask application that uses an application factory and a configuration file.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Runs the Flask application using the configuration variables found in `config.py`:

- `python -B -m flask --app "tracker_03:create_app(config_name='development')" run`
- `python -B -m flask --app "tracker_03:create_app('development')" run`
- `python -B -m flask --app tracker_03 run  # Uses the 'default' configuration`
- `python -B -m flask --app "tracker_03:create_app(foo='42')" run  # Uses the 'foo' command-line argument`

> **NOTE** - Enclose options in quotation marks when using special characters.

-----

## Notes

The Application Factory pattern allows you to use different runtime configurations without having to modify the application's code. For example, instead of creating separate versions of the application for debugging, testing, and production (which increasing maintenance), you can modify the `create_app` method to accept configuration settings, like `logging_level`. You can then pass the settings to the application at runtime, like `create_app(logging_level=logging.DEBUG)` when debugging.

However, your runtime configurations may have a lot of settings, like database locations, server addresses, etc. To avoid long command lines, you can organize these settings into separate classes within a `config.py` file. Then, you would then modify the `create_app` method to accept a configuration *name*, like `development`, and pass it to the application at runtime, like `create_app(config_name=development)` when debugging. This way, you can easily switch between configurations without changing the application code.

Another advantage of using an application factory is that you can add additional command-line arguments other than `config_name`:

```python
def create_app(config_name: str = 'default', foo: str = 'bar') -> flask.Flask:
```

- If you run `python -B -m flask --app tracker_03 run`, `foo` will equal `bar`.
- If you run `python -B -m flask --app "tracker_03:create_app(foo='42')" run`, `foo` will equal `42`.

Your application structure should be like the following:

```text
tracker
├── tracker_01
├── ...
├── tracker_03
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

- `python -B -m flask --app "tracker_03:create_app(config_name='development')" run`
- `python -B -m flask --app "tracker_03:create_app('development')" run`
- `python -B -m flask --app tracker_03 run`
- `python -B -m flask --app "tracker_03:create_app(foo='42')" run`

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by presssing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
