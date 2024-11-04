# Tracker v03

This is a demo of a Flask application that uses an application factory and a configuration file.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Runs the Flask application using the configuration file found in `tracker/tracker_03/config.py`:

- `python -B -m flask --app "tracker_03:create_app(config_name='development')" run`
- `python -B -m flask --app "tracker_03:create_app('testing')" run`
- `python -B -m flask --app tracker_03 run`

> **NOTE** - Enclose options in quotation marks when using special characters.

-----

## Notes

The Application Factory pattern allows you to use different runtime configurations without having to modify the application's code. For example, instead of creating separate versions of the application for debugging, testing, and production (which increasing maintenance), you can modify the `create_app` method to accept configuration settings, like `logging_level`. You can then pass the settings to the application at runtime, like `create_app(logging_level=logging.DEBUG)` when debugging.

However, your runtime configurations may have a lot of settings, like database locations, server addresses, etc. To avoid long command lines, you can organize these settings into separate classes within a `config.py` file. Then, you would then modify the `create_app` method to accept a configuration *name*, like `development`, and pass it to the application at runtime, like `create_app(config_name=development)` when debugging. This way, you can easily switch between configurations without changing the application code.

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

Once you are finished reviewing the code, run your application using different configurations. Do not forget to activate your Python virtual environment first!

> **NOTE** - Enclose options in quotation marks when using special characters.

```shell
python -B -m flask --app "tracker_03:create_app('development')" run
python -B -m flask --app "tracker_03:create_app('testing')" run
python -B -m flask --app tracker_03 run
```

When you are finished testing the application, move on to the next version.
