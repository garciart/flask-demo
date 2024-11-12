# Tracker v09

This is a demo of a Flask application that incorporates blueprints.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Runs the Flask application using routes and HTML files found in the `blueprints` directory:

- `python -B -m flask --app tracker_09 run`

-----

## Notes

After moving your HTML code, the next logical step is to move your page code and routing out of `__init__.py`. Flask ***Blueprints*** allow you to further organize your code by consolidating HTML, routing, and logic into their own packages.

Your application structure should be like the following:

```text
tracker
├── tracker_01
├── ...
├── tracker_09
|   ├── blueprints
|   |   ├── error
|   |   |   ├── templates
|   |   |   |   ├── 404.html
|   |   |   |   └── 500.html
|   |   |   ├── __init__.py
|   |   |   └── error.py
|   |   └── main
|   |       ├── templates
|   |       |   ├── index.html
|   |       |   └── about.html
|   |       ├── __init__.py
|   |       └── main.py
|   ├── static
|   |   ├── css
|   |   |   └── main.css
|   |   ├── img
|   |   |   ├── favicon.ico
|   |   |   └── logo.png
|   |   └── js
|   |       └── main.js
|   ├── tests
|   |   ├── __init__.py
|   |   └── test_app.py
|   ├── templates
|   |   └── base.html
|   ├── __init__.py
|   ├── config.py
|   └── profiler.py
├── tracker_logs
|   └── tracker_09_1234567890.1234567.log
├── venv
|   └── ...
├── .env
├── .flaskenv
├── .gitignore
├── hello.py
└── requirements.txt
```

Review the code and run your application. Do not forget to activate your Python virtual environment first!

- `python -B -m flask --app tracker_09 run`

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by presssing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
