# Tracker_15

This is a demo of a Flask application that uses an API to update a member.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

You can update a database by sending a PUT request with a JSON payload containing the information you want to update to an API endpoint. For example, if you wanted to make a member an administrator, you would make the following requests:

In Linux:

```shell
curl -X PUT -H "Content-Type: application/json" -d '{"member_name": "Leto.Atreides", \
    "member_email": "leto.atreides@atreides.com", "member_is_admin: true}' \
    http://localhost:5000/api/members/2
```

In Windows:

```shell
Invoke-WebRequest -Uri "http://localhost:5000/api/members/2" `
    -Method Put `
    -ContentType "application/json" `
    -Body "{`"member_name`": `"Leto.Atreides`", `"member_email`": `
    `"leto.atreides@atreides.com`", `"member_is_admin`": true}"
```

You can also use applications like **Postman** to simulate requests.

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_15
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
|   └── tracker_15_1234567890.1234567.log
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
python -B -m pylint tracker_15

# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest discover tracker_15/tests -b -v

# See the coverage report in the console
coverage report -m

# Running the unit tests will create the database if it does not exist
# If so, initialize migration support for the application
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_15 db init --directory tracker_15/migrations
python -B -m flask --app tracker_15 db init -d tracker_15/migrations

# Perform an initial migration to capture the current schema of the database
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_15 db migrate --message "Initial migration" --directory tracker_15/migrations
python -B -m flask --app tracker_15 db migrate -m "Initial migration" -d tracker_15/migrations
# For help with any of these commands, use python -B -m flask --app tracker_15 db --help

# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_15:create_app('profiler')" run --without-threads

# Run the Flask application using HTML files found in the `templates` directory
python -B -m flask --app tracker_15 run
```

Based on your operating system, send the PUT request we spoke about earlier to make the member an administrator.

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
