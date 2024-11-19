# Tracker_06

This is a demo of a Flask application that incorporates logging.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

```shell
# Check the application for errors
python -B -m pylint tracker_06
# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest --verbose --buffer tracker_06/tests/test_app.py
# See the coverage report in the console
coverage report -m
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_06:create_app('profiler')" run
# Create a log when running the Flask application
# python -B -m flask --app "tracker_06:create_app(config_name='development', log_events=True)" run
python -B -m flask --app "tracker_06:create_app('development', True)" run
```

> **NOTES**
>
> - Enclose options in quotation marks when using special characters.
> - Do not log events when unit testing or each test will create a log file.
> - Use the `development` configuration during development or the application will create an empty log file, since the application only logs `logging.INFO`-level messages or less.

-----

## Notes

Logging allows you to:

- Capture errors and bugs in your application
- Track how users interact with your application
- Monitor your application's performance

With this information, you can protect, fix, and optimize your web application. The Python Standard Library contains a `logging` module that makes it easy to integrate logging into your application.

We added logging support in `app_utils.py`. We also moved utility functions into this file, like `check_system()` and `validate_input()`, so they are accessible by other files.

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_06
|   ├── tests
|   |   ├── __init__.py
|   |   └── test_app.py
|   ├── __init__.py
|   ├── app_utils.py
|   ├── config.py
|   └── profiler.py
├── tracker_logs
|   └── tracker_06_1234567890.1234567.log
├── .coverage
├── .coveragerc
├── .env
├── .env_alt
├── .flaskenv
├── __init__.py
├── hello.py
└── requirements.txt
```

Once you are finished reviewing the code, start your application. Do not forget to activate your Python virtual environment first!

> **NOTE** - Enclose options in quotation marks when using special characters.

```shell
# Check the application for errors
python -B -m pylint tracker_06
# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest --verbose --buffer tracker_06/tests/test_app.py
# See the coverage report in the console
coverage report -m
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_06:create_app('profiler')" run
# Create a log when running the Flask application
# python -B -m flask --app "tracker_06:create_app(config_name='development', log_events=True)" run
python -B -m flask --app "tracker_06:create_app('development', True)" run
```

Once you have started the server:

- Navigate to your home page at <http://127.0.0.1:5000> and click on refresh a few times.
- Navigate to <http://127.0.0.1:5000/oops>; you should get a `Not Found` error.
- Navigate back to your home page at <http://127.0.0.1:5000> and click on refresh a few times.
- Terminate the application using <kbd>CTRL</kbd> +  <kbd>C</kbd>.
- Take a look at the log file in `tracker_logs`. You should see something like the following:

    ```text
    "date_time", "server_ip", "process_id", "msg_level", "message"
    "2024-11-03 16:50:50,764", "192.168.56.1", "15628", "INFO", "Starting tracker_06 application."
    "2024-11-03 16:51:05,512", "192.168.56.1", "15628", "INFO", "/ requested by 127.0.0.1 using GET; 200 OK."
    "2024-11-03 16:51:06,122", "192.168.56.1", "15628", "INFO", "/ requested by 127.0.0.1 using GET; 200 OK."
    "2024-11-03 16:51:12,914", "192.168.56.1", "15628", "INFO", "/oops requested by 127.0.0.1 using GET; 404 NOT FOUND."
    "2024-11-03 16:51:18,238", "192.168.56.1", "15628", "INFO", "/ requested by 127.0.0.1 using GET; 200 OK."
    "2024-11-03 16:51:20,199", "192.168.56.1", "15628", "INFO", "/ requested by 127.0.0.1 using GET; 200 OK."
    ```

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
