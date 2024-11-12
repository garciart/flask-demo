# Tracker v01

This is a demo of a basic Flask application that uses a package pattern.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

| Run Commands                                                              | Explanation               |
|----------------------------------------------------------------------|---------------------------|
| `flask --app tracker_01 run`                                         | Standard command to run a Flask application, accessible via localhost on the default port (`127.0.0.1:5000`). |
| `python -B -m flask --app tracker_01 run`                            | (*Preferred*) Performs the same action as the standard command, but it uses the `-B` option to prevent writing intermediate bytecode to a `__pycache__` folder. |
| `python -B -m flask --app tracker_01 run --debug`                    | Runs the Flask application in debug mode using the built-in Werkzeug development server. This enables verbose error information and allows "hot reloading," so you don't need to restart the server after every code change. |
| `python -B -m flask --app tracker_01 run --host=0.0.0.0`             | Allows external access to the Flask application via the host's IP address on port `5000`, such as `192.168.0.1:5000`. |
| `python -B -m flask --app tracker_01 run --host=0.0.0.0 --port=5001` | Allows external access to the Flask application on port `5001`. |

-----

## Notes

Most introductory Flask demos use a *module pattern*, with all of the code in a single file named `app.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index() -> str:
    return '<h1>Hello, World!</h1>'
```

The single-file module pattern is great for small demos, but it is not practical for larger applications.

With a *package pattern*, you can split your application into separate files that work together. This allows you to reuse components, helping you to avoid duplicating code. You can also organize the code by purpose, like for views, routing or models, making your application easier to maintain. The package pattern also allows you create different versions of your application for development, testing, and production environments.

To create a simple package:

- Create a sub-directory in your project, named after either your application (`tracker`), the version number (`tracker_01`), or the purpose of the package (`tracker_test`).
- Add a file named `__init__.py` to the directory. This file lets Python know that the directory is a package. By the way, any code in the `__init__.py` file is run first when you run the Flask.
- Place the `app.py` code in the `__init__.py` file.

Your application structure should be like the following:

```text
tracker
├── tracker_01
|   ├── __init__.py
|   └── config.py
├── venv
|   └── ...
├── hello.py
└── requirements.txt
```

Review the code and run your application. Do not forget to activate your Python virtual environment first!

- `python -B -m flask --app tracker_01 run`

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by presssing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
