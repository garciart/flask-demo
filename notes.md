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
