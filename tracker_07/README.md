# Tracker_07

This is a demo of a Flask application that incorporates performance profiling.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

Your website should run very fast using Flask's built-in Werkzeug server; so fast that you may not notice bottlenecks, like large image loading, until you deploy your application on a production server. However, there are several ways to identify slow-loading component, like using the developer tools found in most browsers. Another way is to use the built-in Werkzeug profiler.

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_07
|   ├── tests
|   |   ├── __init__.py
|   |   ├── test_app.py
|   |   ├── test_app_utils.py
|   |   └── test_profiler.py
|   ├── __init__.py
|   ├── app_utils.py
|   ├── config.py
|   └── profiler.py
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

> **NOTES:**
>
> - Enclose options in quotation marks when using special characters.
> - Coverage will create a `__pycache__` folder. Delete it when you are done testing.

```shell
# Check the application for issues
python -B -m pylint tracker_07
coverage run -m unittest discover tracker_07/tests -b -v
coverage report -m
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_07:create_app('profile')" run --without-threads
```

> **NOTE** - There is a [known issue with cProfile and threading](https://github.com/pallets/werkzeug/issues/2909 "ProfilerMiddleware raises ValueError: Another profiling tool is already active") that can interfere with rendering images or running JavaScript files in Flask applications.
>
> Profiling tools like cProfile and Werkzeug's ProfilerMiddleware rely on global states, which can conflict with Flask's default multithreaded server. By disabling threading with the `--without-threads` option, Flask runs in single-threaded mode, ensuring that profiling is not triggered multiple times simultaneously.
>
> Flask's built-in server is designed for development purposes, and running it in single-threaded mode should not affect your application's behavior during testing or debugging. However, **do not use** the built-in server or this setting in production, as it limits the server's ability to handle multiple concurrent requests.

```text
--------------------------------------------------------------------------------
PATH: '/index'
         470 function calls (414 primitive calls) in 0.002 seconds

   Ordered by: internal time, call count
   List reduced from 160 to 30 due to restriction <30>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     26/3    0.000    0.000    0.000    0.000 {built-in method _abc._abc_subclasscheck}
     26/3    0.000    0.000    0.000    0.000 <frozen abc>:121(__subclasscheck__)
       36    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
   ...
        1    0.000    0.000    0.000    0.000 /usr/lib64/python3.12/typing.py:1269(__init__)
      4/1    0.000    0.000    0.000    0.000 /tracker/.venv/lib64/python3.12/site-packages/werkzeug/routing/matcher.py:79(_match)
        1    0.000    0.000    0.000    0.000 /tracker/.venv/lib64/python3.12/site-packages/flask/ctx.py:251(push)

--------------------------------------------------------------------------------

127.0.0.1 - - [15/Nov/2024 22:01:55] "GET /index HTTP/1.1" 200 -
```

The columns in this report are:

| Column                    | Description                                                                                                                                                                                  |
|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ncalls                    | The number of times the function was called. Two numbers mean the function recursed; the first is the total number of calls and the second is the number of primitive (non-recursive) calls. |
| tottime                   | The total time spent in the given function (and excluding time made in calls to sub-functions)                                                                                               |
| percall                   | The quotient of tottime divided by ncalls                                                                                                                                                    |
| cumtime                   | The cumulative time spent in this and all subfunctions (from invocation till exit). This figure is accurate even for recursive functions.                                                    |
| percall                   | The quotient of cumtime divided by primitive calls                                                                                                                                           |
| filename:lineno(function) | Provides the respective data of each function                                                                                                                                                |

Like I said, right now your website runs very fast using Flask's built-in Werkzeug server.

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.
