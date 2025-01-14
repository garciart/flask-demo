# Tracker_99

> **IMPORTANT**:
> - NEED TO ADD UNIT TESTS TO TRACKER 16 AND LATER!

This is a demo of a Flask application that allows you to control course assignments using role-based access control (RBAC).

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_99
|   ├── blueprints
|   |   ├── admin
|   |   |   ├── templates
|   |   |   |   ├── add_course.html
|   |   |   |   ├── add_member.html
|   |   |   |   ├── add_role.html
|   |   |   |   ├── assign_course.html
|   |   |   |   ├── delete_course.html
|   |   |   |   ├── delete_member.html
|   |   |   |   ├── delete_role.html
|   |   |   |   ├── edit_course.html
|   |   |   |   ├── edit_member.html
|   |   |   |   ├── edit_role.html
|   |   |   |   ├── update_profile.html
|   |   |   |   ├── view_course.html
|   |   |   |   ├── view_member.html
|   |   |   |   └── view_role.html
|   |   |   ├── __init__.py
|   |   |   ├── admin_forms.py
|   |   |   ├── admin_routes.py
|   |   |   ├── course_routes.py
|   |   |   ├── member_routes.py
|   |   |   └── role_routes.py
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
|   |   |   └── default.css
|   |   ├── img
|   |   |   ├── favicon.ico
|   |   |   └── logo.png
|   |   └── js
|   |       └── site.js
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
|   └── tracker_99_1234567890.1234567.log
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
python -B -m pylint tracker_99

# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest discover tracker_99/tests -b -v

# See the coverage report in the console
coverage report -m

# Running the unit tests will create the database if it does not exist
# If so, initialize migration support for the application
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_99 db init --directory tracker_99/migrations
python -B -m flask --app tracker_99 db init -d tracker_99/migrations

# Perform an initial migration to capture the current schema of the database
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_99 db migrate --message "Initial migration" --directory tracker_99/migrations
python -B -m flask --app tracker_99 db migrate -m "Initial migration" -d tracker_99/migrations
# For help with any of these commands, use python -B -m flask --app tracker_99 db --help

# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_99:create_app('profile')" run --without-threads

# Run the Flask application using HTML files found in the `templates` directory
python -B -m flask --app tracker_99 run
```

Based on your operating system, run the following commands in another Terminal. You should be able to view yourself, but not other users unless you are an administrator:

**Linux:**

```bash
# This command will generate a JSON Web Token (JWT) for Admin
curl -X PUT -H "Content-Type: application/json" -d '{"username": "admin", \
    "password": "Change.Me.321"}' http://127.0.0.1:5000/api/login

# Run the following commands using the generated JWT
# View all members will work
curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/members/all

# View a single member will work
curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/members/2

# This command will generate a JSON Web Token (JWT) for a member
curl -X PUT -H "Content-Type: application/json" -d '{"username": "leto.atreides", \
    "password": "Change.Me.123"}' http://127.0.0.1:5000/api/login

# Run the following commands using the generated JWT
# View all members will NOT work
curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/members/all

# View yourself will work
curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/members/2

# View another member will NOT work
curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/members/3
```

**Windows:**

```shell
# This command will generate a JSON Web Token (JWT) for Admin
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/login" `
    -Method Post `
    -ContentType "application/json" `
    -Body "{`"username`": `"admin`", `"password`": `"Change.Me.321`"}"

# View all members will work
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/members/all" `
    -Method GET `
    -Headers @{ "Authorization" = "Bearer json.web.token" }

# View a single member wil work
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/members/2" `
    -Method GET `
    -Headers @{ "Authorization" = "Bearer json.web.token" }

# This command will generate a JSON Web Token (JWT) for a member
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/login" `
    -Method Post `
    -ContentType "application/json" `
    -Body "{`"username`": `"leto.atreides`", `"password`": `"Change.Me.123`"}"

# Run the following commands using the generated JWT
# View all members will NOT work
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/members/all" `
    -Method GET `
    -Headers @{ "Authorization" = "Bearer json.web.token" }

# View yourself will work
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/members/2" `
    -Method GET `
    -Headers @{ "Authorization" = "Bearer json.web.token" }

# View another member will NOT work
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/members/3" `
    -Method GET `
    -Headers @{ "Authorization" = "Bearer json.web.token" }
```

Open a browser and navigate to <http://127.0.0.1:5000>. Login as admin, perform some tasks, and log off. Log back in as a member and try to perform the same tasks. Some will work, while others will not.

Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
