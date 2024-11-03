# Tracker v03

This is a demo of a basic Flask application that uses an application factory and a configuration file.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Runs the Flask application using the configuration file found in `tracker/tracker_03/config.py`:

- `python -B -m flask --app tracker_03 run`
- `python -B -m flask --app "tracker_03:create_app(config_name='development')" run`
- `python -B -m flask --app "tracker_03:create_app('development')" run`

> **NOTE** - Enclose options in quotation marks when using special characters.

-----

## Notes

The Application Factory pattern...

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

Once you are finished, run your application. Do not forget to activate your Python virtual environment first!

```shell
python -B -m flask --app tracker_03 run
```
