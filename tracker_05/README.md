# Tracker_05

This is a demo of a Flask application that incorporates performance profiling.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

```shell
# Check the application for errors
python -B -m pylint tracker_05
# Run the unit tests found in `tests/test_app.py` using Coverage
coverage run -m unittest --verbose --buffer tracker_05/tests/test_app.py
# See the coverage report in the console
coverage report -m
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_05:create_app('profiler')" run
```

> **NOTE** - Enclose options in quotation marks when using special characters.

-----

## Notes

Your website should run very fast using Flask's built-in Werkzeug server; so fast that you may not notice bottlenecks, like large image loading, until you deploy your application on a production server. However, there are several ways to identify slow-loading component, like using the developer tools found in most browsers. Another way is to use the built-in Werkzeug profiler.

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_05
|   ├── tests
|   |   ├── __init__.py
|   |   └── test_app.py
|   ├── __init__.py
|   ├── config.py
|   └── profiler.py
├── .coverage
├── .coveragerc
├── .env
├── .env_alt
├── .flaskenv
├── .gitignore
├── __init__.py
├── hello.py
└── requirements.txt
```

Review the code and run your application. Do not forget to activate your Python virtual environment first!

```shell
# Run the unit tests found in `tests/test_app.py` using Coverage
coverage run -m unittest --verbose --buffer tracker_05/tests/test_app.py
# See the coverage report in the console
coverage report -m
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_05:create_app('profiler')" run
```

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
