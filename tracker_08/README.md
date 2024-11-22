# Tracker_08

This is a demo of a Flask application that incorporates templates.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

```shell
# Check the application for issues
python -B -m pylint tracker_08
# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest --verbose --buffer tracker_08/tests/test_app.py
# See the coverage report in the console
coverage report -m
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_08:create_app('profiler')" run
# Run the Flask application using HTML files found in the `templates` directory
# python -B -m flask --app "tracker_08:create_app(config_name='development', log_events=True)" run
python -B -m flask --app "tracker_08:create_app('development', True)" run
```

> **NOTE** - Enclose options in quotation marks when using special characters.

-----

## Notes

Keeping your website's code in `__init__.py` is impractical, especially if you have dozens of pages with extensive Hypertext Markup Language (HTML) code. Flask ***Templates*** allow you to organize your code in a sensible manner. They are easier to maintain and reusable. Templates also allow you to incorporate Cascading Style Sheets (CSS), images, and JavaScript code to enhance the experience of your users when they visit your website.

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_08
|   ├── static
|   |   ├── css
|   |   |   └── main.css
|   |   ├── img
|   |   |   ├── favicon.ico
|   |   |   └── logo.png
|   |   └── js
|   |       └── main.js
|   ├── tests
|   |   ├── __init__.py
|   |   └── test_app.py
|   ├── templates
|   |   ├── error
|   |   |   ├── 404.html
|   |   |   └── 500.html
|   |   ├── main
|   |   |   └── index.html
|   |   └── base.html
|   ├── __init__.py
|   ├── app_utils.py
|   ├── config.py
|   └── profiler.py
├── tracker_logs
|   └── tracker_08_1234567890.1234567.log

├── .coverage
├── .coveragerc
├── .env
├── .env_alt
├── .flaskenv
├── __init__.py
├── hello.py
└── requirements.txt
```

Check the code for issues, then run your application. Do not forget to activate your Python virtual environment first!

```shell
# Check the application for issues
python -B -m pylint tracker_08
# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest --verbose --buffer tracker_08/tests/test_app.py
# See the coverage report in the console
coverage report -m
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_08:create_app('profiler')" run
# Run the Flask application using HTML files found in the `templates` directory
# python -B -m flask --app "tracker_08:create_app(config_name='development', log_events=True)" run
python -B -m flask --app "tracker_08:create_app('development', True)" run
```

Run your application using the `development` configuration, refresh the page, and terminate the application using <kbd>CTRL</kbd> +  <kbd>C</kbd>. Take a look at the log file in `tracker_logs`. You should see something like the following:

```text
"date_time", "server_ip", "process_id", "msg_level", "message"
"2024-11-03 18:38:21,123", "192.168.56.1", "17384", "INFO", "Starting tracker_08 application."
"2024-11-03 18:38:23,836", "192.168.56.1", "17384", "INFO", "/ requested by 127.0.0.1 using GET; 200 OK."
"2024-11-03 18:38:24,436", "192.168.56.1", "17384", "INFO", "/static/img/logo.png requested by 127.0.0.1 using GET; 200 OK."
"2024-11-03 18:38:24,440", "192.168.56.1", "17384", "INFO", "/static/css/main.css requested by 127.0.0.1 using GET; 200 OK."
"2024-11-03 18:38:24,440", "192.168.56.1", "17384", "INFO", "/static/js/main.js requested by 127.0.0.1 using GET; 200 OK."
"2024-11-03 18:38:35,856", "192.168.56.1", "17384", "INFO", "/index requested by 127.0.0.1 using GET; 200 OK."
"2024-11-03 18:38:35,868", "192.168.56.1", "17384", "INFO", "/static/css/main.css requested by 127.0.0.1 using GET; 304 NOT MODIFIED."
"2024-11-03 18:38:35,870", "192.168.56.1", "17384", "INFO", "/static/img/logo.png requested by 127.0.0.1 using GET; 304 NOT MODIFIED."
"2024-11-03 18:38:35,871", "192.168.56.1", "17384", "INFO", "/static/js/main.js requested by 127.0.0.1 using GET; 304 NOT MODIFIED."
"2024-11-03 18:38:35,881", "192.168.56.1", "17384", "INFO", "/static/img/logo.png requested by 127.0.0.1 using GET; 304 NOT MODIFIED."
```

The HTTP response code `304 NOT MODIFIED` means that the server found a cached copy of the resource, like a favicon, so it did not request a new version from the server. This speeds up rendering the page. On most browsers, if you want the application to re-request the resource, press <kbd>Shift</kbd> <kbd>F5</kbd>; that forces the application to ignore the cache and retrieve a fresh version of the web page.

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
