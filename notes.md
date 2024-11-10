# Notes

Create the development environment:

```bash
mkdir -p ~/repos/flask-template
cd ~/repos/flask-template
python3 -m venv $PWD
source bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
# Ensure the linters are in your environment
python3 -m pip install pylint
python3 -m pip install flake8
```

Make requirements file:

```bash
python3 -m pip freeze > requirements.txt
```

Add `.gitignore` file.
Add `.flaskenv` file.
Add `app.py` script.
Add `app` directory.
Add `app/__init__.py` script.
Add `app/config.py` script.
Add `app/app_utils.py` script.
Add `app/routes.py` script.
Add `app/routes_api.py` script.
Add `app/routes_err.py` script.
Add `app/static` directory.
Add `app/static/css` directory.
Add `app/static/css/base.css` file.
Add Bootstrap and DataTables CSS files.
Add `app/static/img` directory.
Add `error.gif`, `favicon.ico`, and `logo.png` files.
Add `app/static/js` directory.
Add `app/static/css/base.js` script.
Add Bootstrap, DataTables, and jQuery JavaScript scripts.
Add `app/templates` directory.
Add `app/templates/base.html` file.

TODO: Add routing and templates.
TODO: Add migration and database creation.

Add `app/tests` directory.
Add `app/tests/__init__.py` script.
Add `app/tests/test_app.py` script.
Add `app/tests` directory.

## Best Practices

Use a virtual environment
Change maximum line length to 100 characters
Use PEP-8 naming conventions
Write docstrings per PEP 257 using reStructuredText style.
Include "Usage:" comments in the header docstring of modules
Include type hints when defining the parameters of an function or method
Pass keyword arguments instead of depending on positional parsing
Consolidate repeated code into functions or methods (DRY)
Organize related code and modules into packages
Use relative imports; check them after any changes!
Stick to the Standard Library when possible
Use input validation
Do not hard code sensitive information
Use parentheses instead of slashes for long line continuations
Use simple and readable code instead of LEET code
Use comments often

Include logging module
Include profiling to find bottlenecks


Lint code with PyLint after making any changes
Add, update, and run unit tests for edge cases with unittest after making any changes
Run application using the 'development' configuration first and check the logs
Do not log when running the application in hotfix or 'debug' mode