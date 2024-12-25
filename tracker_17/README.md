# Tracker_17

> **IMPORTANT**:
> - NEED TO ADD UNIT TESTS TO TRACKER 16 AND LATER!
> - Do not forget to add an endpoint to API routes or you will get an AssertionError!

This is a demo of a Flask application that incorporates API authentication.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

To prevent anyone from editing member data using the API, we will add authentication to the API.

To get started, install the [Python JSON Web Token (JWT) package](https://pyjwt.readthedocs.io):

```shell
python -m pip install pyjwt
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
├── tracker_17
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
|   └── tracker_17_1234567890.1234567.log
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
python -B -m pylint tracker_17

# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest discover tracker_17/tests -b -v

# See the coverage report in the console
coverage report -m

# Running the unit tests will create the database if it does not exist
# If so, initialize migration support for the application
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_17 db init --directory tracker_17/migrations
python -B -m flask --app tracker_17 db init -d tracker_17/migrations

# Perform an initial migration to capture the current schema of the database
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_17 db migrate --message "Initial migration" --directory tracker_17/migrations
python -B -m flask --app tracker_17 db migrate -m "Initial migration" -d tracker_17/migrations
# For help with any of these commands, use python -B -m flask --app tracker_17 db --help

# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_17:create_app('profile')" run --without-threads

# Run the Flask application using HTML files found in the `templates` directory
python -B -m flask --app tracker_17 run
```

```txt
Linux:
curl -X PUT -H "Content-Type: application/json" -d '{"username": "admin", \
    "password": "foobar"}' http://127.0.0.1:5000/api/login

curl -X GET -H "Authorization: Bearer your.jwt.token.here"' \
    http://127.0.0.1:5000/api/members/all

curl -X GET -H "Authorization: Bearer your.jwt.token.here"' \
    http://127.0.0.1:5000/api/members/2

curl -X PUT -H "Content-Type: application/json" \
    -H "Authorization: Bearer your.jwt.token.here" \
    -d '{"member_name": "Leto.Atreides", \
    "member_email": "leto.atreides@atreides.com", "member_is_admin": true}' \
    http://localhost:5000/api/members/2

Windows:
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/login" `
    -Method Post `
    -ContentType "application/json" `
    -Body "{`"username`": `"admin`", `"password`": `"Change.Me.321`"}"

Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/members/all" `
    -Method GET `
    -Headers @{ "Authorization" = "Bearer your.jwt.token.here" }

Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/members/2" `
    -Method GET `
    -Headers @{ "Authorization" = "Bearer your.jwt.token.here" }

Invoke-WebRequest -Uri "http://localhost:5000/api/members/2" `
    -Method Put `
    -ContentType "application/json" `
    -Headers @{ "Authorization" = "Bearer your.jwt.token.here" } `
    -Body "{`"member_name`": `"Leto.Atreides`", `"member_email`": `
    `"leto.atreides@atreides.com`", `"member_is_admin`": true}"
```

Based on your operating system, send the PUT request we spoke about earlier to make the member an administrator.

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
