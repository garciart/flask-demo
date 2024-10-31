# Tracker v01

This is a demo of a basic Flask application that uses a package pattern.

## Usage

- `flask --app 'tracker_01' run  # Allow access via localst host on port 5000`
- `python3 -B -m flask --app 'tracker_01' run  # Does not create a __pycache__ folder`
- `python3 -B -m flask --app 'tracker_01' run --debug  # Allows hot reloads`
- `python3 -B -m flask --app 'tracker_01' run --host=0.0.0.0  # Allows outside access via the host IP address on port 5000`
- `python3 -B -m flask --app 'tracker_01' run --host=0.0.0.0 --port=5001  # Allows outside access via the host IP address on port 5001`

## Notes

Most introductory Flask demos use a *module pattern*, with all of the code in a single file named `app.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index() -> str:
    return '<h1>Hello, World!</h1>'
```

The module pattern is great for small demos, but it is not practical for larger applications.

With a *package pattern*, you can split your application into different parts, like HTML templates and Python code. This helps you avoid repeating code and makes your application easier to manage. It also lets you create different versions of your application for development, testing, and production.

To use a simple package:

- Create a sub-directory in your project, with the name of your application, like `tracker`, the version number, like `tracker_01`, or the purpose of the package, like `tracker_test`.
- Add a file named `__init__.py` to the directory.
- Place the `app.py` code in the `__init__.py` file.

Your application structure should be like the following:

```text
tracker
├── tracker_01
|   ├── __init__.py
|   └── config.py
├── venv
|   └── ...
├── .flaskenv
├── .gitignore
├── hello.py
└── requirements.txt
```
