# Tracker_14

This is a demo of a Flask application that incorporates Forms.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

From <https://wtforms.readthedocs.io/>: *"WTForms is a flexible forms validation and rendering library for Python web development. It can work with whatever web framework and template engine you choose. It supports data validation, CSRF protection, internationalization (I18N), and more."*

In this version, we will add a form that allows you to edit a member's profile.

To get started, install WTForms:

```shell
python -m pip install Flask-WTF
# Install additional packages for WTF
python -m pip install email-validator
# Update the required packages list
python -m pip freeze > requirements.txt
```

Do not forget to register the new Admin blueprint in `__init__.py`. Also, include a reference to the `SECRET_KEY` with a default value in `config.py` so you can perform unit tests (`unittest` and `coverage` will not read `.env` files).

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_14
|   ├── blueprints
|   |   ├── admin
|   |   |   ├── templates
|   |   |   |   ├── edit_member.html
|   |   |   |   └── view_member.html
|   |   |   ├── __init__.py
|   |   |   ├── admin_forms.py
|   |   |   └── admin_routes.py
|   |   ├── api
|   |   |   ├── __init__.py
|   |   |   └── api_routes.py
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
|   ├── migrations
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
|   |   ├── test_admin.py
|   |   ├── test_api.py
|   |   ├── test_app.py
|   |   ├── test_app_utils_1.py
|   |   ├── test_app_utils_2.py
|   |   ├── test_error.py
|   |   ├── test_main.py
|   |   ├── test_models_member.py
|   |   └── test_profiler.py
|   ├── __init__.py
|   ├── app_utils.py
|   ├── config.py
|   ├── profiler.py
|   └── tracker.db
├── tracker_logs
|   └── tracker_14_1234567890.1234567.log
├── __init__.py
├── .coverage
├── .coveragerc
├── .env
├── .env_alt
├── .flaskenv
├── .pylintrc
├── hello.py
└── requirements.txt
```

Check the code for issues, then run your application. Do not forget to activate your Python virtual environment first!

```shell
# Check the application for issues
python -B -m pylint tracker_14

# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest discover tracker_14/tests -b -v

# See the coverage report in the console
coverage report -m

# Running the unit tests will create the database if it does not exist
# If so, initialize migration support for the application
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_14 db init --directory tracker_14/migrations
python -B -m flask --app tracker_14 db init -d tracker_14/migrations

# Perform an initial migration to capture the current schema of the database
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_14 db migrate --message "Initial migration" --directory tracker_14/migrations
python -B -m flask --app tracker_14 db migrate -m "Initial migration" -d tracker_14/migrations
# For help with any of these commands, use python -B -m flask --app tracker_14 db --help

# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_14:create_app('profiler')" run --without-threads

# Run the Flask application using HTML files found in the `templates` directory
python -B -m flask --app tracker_14 run
```

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
