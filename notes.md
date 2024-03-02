# Notes

Create the development environment:

```bash
mkdir -p ~/repos/flask-template
cd ~/repos/flask-template
python3 -m venv $PWD
source bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install flask
python3 -m pip install python-dotenv
python3 -m pip install watchdog  # ?
python3 -m pip install flask-login
python3 -m pip install flask-wtf
python3 -m pip install flask-sqlalchemy
python3 -m pip install flask-migrate
pip install email-validator
# Ensure the linters are in your environment
python3 -m pip install pylint
python3 -m pip install flake8
```

Make requirements file:

```bash
python3 -m pip freeze > requirements.txt
```

TODO: Change routing and templating task due to blueprinting.

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
Add `app/templates/index.html` file.
Add `app/templates/about.html` file.
Add `app/templates/errors.html` file.
Add `app/tests` directory.
Add `app/tests/__init__.py` script.
Add `app/tests/test_app.py` script.
Add `app/tests` directory.
Add `app/schema.sql` script.
Add `app/db.py` script.
