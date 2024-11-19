# Tracker_10

This is a demo of a Flask application that incorporates blueprints.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

Runs the Flask application using routes and HTML files found in the `blueprints` directory:

- `python -B -m flask --app tracker_10 run`

-----

## Notes

After moving your HTML code, the next logical step is to move your page code and routing out of `__init__.py`. Flask ***Blueprints*** allow you to further organize your code by consolidating HTML, routing, and logic into their own packages.

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_10
|   ├── blueprints
|   |   ├── error
|   |   |   ├── templates
|   |   |   |   ├── 404.html
|   |   |   |   └── 500.html
|   |   |   ├── __init__.py
|   |   |   └── error_routes.py
|   |   └── main
|   |       ├── templates
|   |       |   ├── about.html
|   |       |   └── index.html
|   |       ├── __init__.py
|   |       └── main_routes.py
|   ├── models
|   |   ├── __init__.py
|   |   ├── create_db.py
|   |   └── member.py
|   ├── static
|   |   ├── css
|   |   |   └── main.css
|   |   ├── img
|   |   |   ├── favicon.ico
|   |   |   └── logo.png
|   |   └── js
|   |       └── main.js
|   ├── templates
|   |   └── base.html
|   ├── tests
|   |   ├── __init__.py
|   |   └── test_app.py
|   ├── __init__.py
|   ├── app_utils.py
|   ├── config.py
|   ├── profiler.py
|   └── tracker.db
├── tracker_logs
|   └── tracker_10_1234567890.1234567.log
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

- `python -B -m flask --app tracker_10 run`

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
