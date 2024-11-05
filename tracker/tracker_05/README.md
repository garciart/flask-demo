# Tracker v05

This is a demo of a Flask application that incorporates logging.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Creates a log when running the Flask application:

- `python -B -m flask --app "tracker_05:create_app(config_name='development', log_events=True)" run`
- `python -B -m flask --app "tracker_05:create_app('development', True)" run`

> **NOTE**
>
> - Enclose options in quotation marks when using special characters.
> - Use the `development` configurations or the application will create an empty log file, since the application only logs `logging.INFO`-level messages or less.

-----

## Notes

Logging allows you to:

- Capture errors and bugs in your application
- Track how users interact with your application
- Monitor your application's performance

With this information, you can protect, fix, and optimize your web application. The Python Standard Library contains a `logging` module that makes it easy to integrate logging into your application.

Your application structure should be like the following:

```text
tracker
├── tracker_01
├── ...
├── tracker_05
|   ├── tests
|   |   ├── __init__.py
|   |   └── test_app.py
|   ├── __init__.py
|   └── config.py
├── tracker_logs
|   └── tracker_05_1234567890.1234567.log
├── venv
|   └── ...
├── .env
├── .flaskenv
├── .gitignore
├── hello.py
└── requirements.txt
```

Once you are finished reviewing the code, start your application. Do not forget to activate your Python virtual environment first!

> **NOTE** - Enclose options in quotation marks when using special characters.

- `python -B -m flask --app "tracker_05:create_app(config_name='development', log_events=True)" run`
- `python -B -m flask --app "tracker_05:create_app('development', True)" run`

Once you have started the server:

- Navigate to your home page at <http://127.0.0.1:5000> and click on refresh a few times.
- Navigate to <http://127.0.0.1:5000/oops>; you should get a `Not Found` error.
- Navigate back to your home page at <http://127.0.0.1:5000> and click on refresh a few times.
- Terminate the application using <kbd>Ctrl</kbd> <kbd>c</kbd>.
- Take a look at the log file in `tracker_logs`. You should see something like the following:

    ```text
    "date_time", "server_ip", "process_id", "msg_level", "message"
    "2024-11-03 16:50:50,764", "192.168.56.1", "15628", "INFO", "Starting tracker_05 application."
    "2024-11-03 16:51:05,512", "192.168.56.1", "15628", "INFO", "/ requested by 127.0.0.1 using GET; 200 OK."
    "2024-11-03 16:51:06,122", "192.168.56.1", "15628", "INFO", "/ requested by 127.0.0.1 using GET; 200 OK."
    "2024-11-03 16:51:12,914", "192.168.56.1", "15628", "INFO", "/oops requested by 127.0.0.1 using GET; 404 NOT FOUND."
    "2024-11-03 16:51:18,238", "192.168.56.1", "15628", "INFO", "/ requested by 127.0.0.1 using GET; 200 OK."
    "2024-11-03 16:51:20,199", "192.168.56.1", "15628", "INFO", "/ requested by 127.0.0.1 using GET; 200 OK."
    ```

When you are finished, move on to the next version.
