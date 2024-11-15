# Tracker_07

This is a demo of a Flask application that incorporates error handling.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Redirects the user to a custom error page and logs the error:

- `python -B -m flask --app "tracker_07:create_app(config_name='development', log_events=True)" run`
- `python -B -m flask --app "tracker_07:create_app('development', True)" run`

> **NOTE**
>
> - Enclose options in quotation marks when using special characters.
> - Use the `development` configurations or the application will not log `logging.INFO`-level messages.

-----

## Notes

Incorporating error handling in your application not only provides feedback to the user, but captures information you can use to debug and improve your site.

Your application structure should be like the following:

```text
tracker
├── tracker_01
├── ...
├── tracker_07
|   ├── tests
|   |   ├── __init__.py
|   |   └── test_app.py
|   ├── __init__.py
|   ├── app_utils.py
|   ├── config.py
|   └── profiler.py
├── tracker_logs
|   └── tracker_07_1234567890.1234567.log
├── venv
|   └── ...
├── .env
├── .flaskenv
├── .gitignore
├── __init__.py
├── hello.py
└── requirements.txt
```

Review the code and run your application. Do not forget to activate your Python virtual environment first!

> **NOTE** - Enclose options in quotation marks when using special characters.

- `python -B -m flask --app "tracker_07:create_app(config_name='development', log_events=True)" run`
- `python -B -m flask --app "tracker_07:create_app('development', True)" run`

Once you have started the server:

- Navigate to your home page at <http://127.0.0.1:5000> and click on refresh a few times.
- Navigate to <http://127.0.0.1:5000/oops>; you should see your custom `Not Found` page.
- Click on the **home page** hyperlink to navigate back to your home page and then click on refresh a few times.
- Navigate to <http://127.0.0.1:5000/doh>; you should see your custom `Internal Server Error` page.
- Click on the **here** hyperlink to navigate back to your home page and then click on refresh a few times.
- Terminate the application using <kbd>CTRL</kbd> +  <kbd>C</kbd>.
- Take a look at the log file in `tracker_logs`. You should see something like the following:

    ```text
    "date_time", "server_ip", "process_id", "msg_level", "message"
    "2024-11-03 16:59:18,639", "192.168.56.1", "15452", "INFO", "Starting tracker_07 application."
    "2024-11-03 16:59:21,163", "192.168.56.1", "15452", "INFO", "/ requested by 127.0.0.1 using GET; 200 OK."
    "2024-11-03 16:59:22,016", "192.168.56.1", "15452", "INFO", "/ requested by 127.0.0.1 using GET; 200 OK."
    "2024-11-03 16:59:29,792", "192.168.56.1", "15452", "INFO", "/oops requested by 127.0.0.1 using GET; 404 NOT FOUND."
    "2024-11-03 16:59:33,491", "192.168.56.1", "15452", "INFO", "/index requested by 127.0.0.1 using GET; 200 OK."
    "2024-11-03 17:00:26,387", "192.168.56.1", "15452", "INFO", "/index requested by 127.0.0.1 using GET; 200 OK."
    "2024-11-03 17:00:32,031", "192.168.56.1", "15452", "ERROR", "Exception on /doh [GET]"
    Traceback (most recent call last):
    ...
    Exception: This is an intentional 500 error.
    "2024-11-03 17:00:32,033", "192.168.56.1", "15452", "INFO", "/doh requested by 127.0.0.1 using GET; 500 INTERNAL SERVER ERROR."
    "2024-11-03 17:01:30,883", "192.168.56.1", "15452", "INFO", "/index requested by 127.0.0.1 using GET; 200 OK."
    "2024-11-03 17:01:33,417", "192.168.56.1", "15452", "INFO", "/index requested by 127.0.0.1 using GET; 200 OK."
    ```

By the way, if you simply ran `python -B -m flask --app tracker_07 run` and navigated to <http://127.0.0.1:5000/doh>, Flask would log the error, since it is a `logging.ERROR`-level message. However, Flask would not log any `logging.INFO`-level messages.

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
