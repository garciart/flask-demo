# Tracker_16

This is a demo of a Flask application that incorporates authentication.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

To prevent anyone from editing member data, we will add authentication to the application.

To get started, install Flask Login:

```shell
python -m pip install flask-login
# Update the required packages list
python -m pip freeze > requirements.txt
```

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_16
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
|   └── tracker_16_1234567890.1234567.log
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
python -B -m pylint tracker_16

# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest discover tracker_16/tests -b -v

# See the coverage report in the console
coverage report -m

# Running the unit tests will create the database if it does not exist
# If so, initialize migration support for the application
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_16 db init --directory tracker_16/migrations
python -B -m flask --app tracker_16 db init -d tracker_16/migrations

# Perform an initial migration to capture the current schema of the database
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_16 db migrate --message "Initial migration" --directory tracker_16/migrations
python -B -m flask --app tracker_16 db migrate -m "Initial migration" -d tracker_16/migrations
# For help with any of these commands, use python -B -m flask --app tracker_16 db --help

# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_16:create_app('profiler')" run --without-threads

# Run the Flask application using HTML files found in the `templates` directory
python -B -m flask --app tracker_16 run
```

Based on your operating system, send the PUT request we spoke about earlier to make the member an administrator.

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
