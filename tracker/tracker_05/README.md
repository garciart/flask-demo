# Tracker v05

This is a demo of a Flask application that incorporates error handling.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Runs the Flask application using the configuration file found in `tracker/tracker_05/config.py`:

- `python -B -m flask --app "tracker_05:create_app(config_name='development')" run`
- `python -B -m flask --app "tracker_05:create_app(config_name='testing')" run`

> **NOTE**
>
> - Enclose options in quotation marks when using special characters.
> - Use the `development` or `testing` configurations or the application will not log the requests, since the logging level must be `logging.INFO` or less.

-----

## Notes

Incorporating error handling in your application not only provides feedback to the user, but captures information you can use to debug and improve your site.

Your application structure should be like the following:

```text
tracker
├── tracker_01
├── ...
├── tracker_05
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

Once you are finished reviewing the code, run your application using different configurations. Do not forget to activate your Python virtual environment first!

> **NOTE** - Enclose options in quotation marks when using special characters.

```shell
python -B -m flask --app "tracker_05:create_app('development')" run
python -B -m flask --app "tracker_05:create_app('testing')" run
```

Once you have started the server:

- Navigate to your home page at <http://127.0.0.1:5000> and click on refresh a few times.
- Navigate to <http://127.0.0.1:5000/oops>; you should see your custom `Not Found` page.
- Click on the **home page** hyperlink to navigate back to your home page and then click on refresh a few times.
- Navigate to <http://127.0.0.1:5000/doh>; you should see your custom `Internal Server Error` page.
- Click on the **here** hyperlink to navigate back to your home page and then click on refresh a few times.
- Terminate the application using <kbd>Ctrl</kbd> <kbd>c</kbd>.
- Take a look at the log file in `tracker_logs`. You should see something like the following:

    ```text
    "date_time", "server_ip", "process_id", "msg_level", "message"
    "2024-11-03 16:59:18,639", "192.168.56.1", "15452", "INFO", "Starting tracker_05 application."
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

When you are finished testing the application, move on to the next version.
