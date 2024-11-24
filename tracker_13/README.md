# Tracker_13

This is a demo of a Flask application that incorporates a Representational State Transfer (ReST) Application Programming Interface (API).

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

You can allow other sites to access the data in your database through Representational State Transfer (REST) Application Programming Interface (API) calls. REST is an architectural style that utilizes standard HTTP methods to enable communication between systems.

This API version contains *endpoints* that return static data in JSON format, such as a list of members in your database.

While your application is running, you can access the data by opening a browser and navigating to <http://127.0.0.1:5000/api/members/all>, or you can access the data using the curl command:

```shell
curl http://127.0.0.1:5000/api/members/all
```

**Output:**

```text
{"members":[{"member_email":"admin@tracker.com","member_id":1,"member_name":"Admin"},{"member_email":"leto.atreides@atreides.com","member_id":2,"member_name":"Leto.Atreides"},{"member_email":"paul.atreides@atreides.com","member_id":3,"member_name":"Paul.Atreides"},{"member_email":"jessica.nerus@atreides.com","member_id":4,"member_name":"Jessica.Nerus"},{"member_email":"thufir.hawat@atreides.com","member_id":5,"member_name":"Thufir.Hawat"},{"member_email":"gurney.halleck@atreides.com","member_id":6,"member_name":"Gurney.Halleck"},{"member_email":"duncan.idaho@atreides.com","member_id":7,"member_name":"Duncan.Idaho"},{"member_email":"vladmir.harkonnen@harkonnen.com","member_id":8,"member_name":"Vladimir.Harkonnen"},{"member_email":"glossu.rabban@harkonnen.com","member_id":9,"member_name":"Glossu.Rabban"},{"member_email":"feyd-rautha.rabban@harkonnen.com","member_id":10,"member_name":"Feyd-Rautha.Rabban"},{"member_email":"piter.devries@harkonnen.com","member_id":11,"member_name":"Piter.DeVries"},{"member_email":"shaddam.corrino@corrino.com","member_id":12,"member_name":"Shaddam.Corrino"},{"member_email":"irulan.corrino@corrino.com","member_id":13,"member_name":"Irulan.Corrino"},{"member_email":"liet.kynes@fremen.com","member_id":14,"member_name":"Liet.Kynes"},{"member_email":"chani.kynes@fremen.com","member_id":15,"member_name":"Chani.Kynes"},{"member_email":"stilgar.tabr@fremen.com","member_id":16,"member_name":"Stilgar.Tabr"}]}
```

Here is an example of an API call that returns only one member:

```shell
curl http://127.0.0.1:5000/api/members/3
```

**Output:**

```text
{"members":[{"member_email":"paul.atreides@atreides.com","member_id":3,"member_name":"Paul.Atreides"}]}
```

Here is an example of an API call that looks for a non-existent member:

```shell
curl http://127.0.0.1:5000/api/members/100
```

**Output:**

```text
{"error":"Member not found"}
```

If you enabled logging, you will see these calls recorded in your application's logs, helping you to monitor API usage and troubleshoot issues.

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_13
|   ├── blueprints
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
|   |   ├── test_app.py
|   |   ├── test_app_utils_1.py
|   |   ├── test_app_utils_2.py
|   |   ├── test_models_member.py
|   |   └── test_profiler.py
|   ├── __init__.py
|   ├── app_utils.py
|   ├── config.py
|   ├── profiler.py
|   └── tracker.db
├── tracker_logs
|   └── tracker_13_1234567890.1234567.log
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
python -B -m pylint tracker_13

# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest discover tracker_13/tests -b -v

# See the coverage report in the console
coverage report -m

# Running the unit tests will create the database if it does not exist
# If so, initialize migration support for the application
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_13 db init --directory tracker_13/migrations
python -B -m flask --app tracker_13 db init -d tracker_13/migrations

# Perform an initial migration to capture the current schema of the database
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_13 db migrate --message "Initial migration" --directory tracker_13/migrations
python -B -m flask --app tracker_13 db migrate -m "Initial migration" -d tracker_13/migrations
# For help with any of these commands, use python -B -m flask --app tracker_13 db --help

# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_13:create_app('profiler')" run --without-threads

# Run the Flask application using HTML files found in the `templates` directory
python -B -m flask --app tracker_13 run
```

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
