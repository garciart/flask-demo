# Tracker v01

This is a demo of a basic Flask application that uses a package and application factory.

## Usage

`python -B -m flask --app "v01" run`

## Notes

Most introductory Flask demos use a single file or *module* named `app.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'
```

While having all of your Python code in one file is convenient for small demos, using a single module for an actual application is not practical or scalable.

A *package*
