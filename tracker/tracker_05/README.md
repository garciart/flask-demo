# Tracker_05

This is a sub-demo of a Flask application that incorporates performance profiling.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Unit tests the Flask application using coverage and the unit tests found in `tests/test_app.py`:

- `coverage run -m unittest --verbose --buffer tracker_05/tests/test_app.py`
- `coverage report -m`
- `coverage html --directory tracker_05/tests/htmlcov`

-----

## Notes

Your website should run very fast using Flask's built-in Werkzeug; so fast that you may not notice bottlenecks, like large image loading, until you deploy your application on a production server. However, there are several ways to identify slow-loading component, like using the developer tools found in most browsers. Another way is to use the built-in Werkzeug profiler.

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
|   ├── config.py
|   └── profiler.py
├── venv
|   └── ...
├── .coverage
├── .env
├── .flaskenv
├── .gitignore
├── __init__.py
├── hello.py
└── requirements.txt
```

Review the code and run your application. Do not forget to activate your Python virtual environment first!

- `python -B -m flask --app "tracker_05:create_app('development')" run`

```text
--------------------------------------------------------------------------------
PATH: '/'
381 function calls (371 primitive calls) in 0.001 seconds

Ordered by: internal time, call count
List reduced from 154 to 30 due to restriction <30>

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\routing\matcher.py:69(match)
    1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
  4/1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\routing\matcher.py:79(_match)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\flask\ctx.py:396(pop)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\routing\map.py:252(bind_to_environ)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\flask\app.py:1233(preprocess_request)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\routing\map.py:492(match)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\sansio\response.py:111(__init__)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\wrappers\request.py:110(__init__)
    1    0.000    0.000    0.001    0.001 tracker\venv\Lib\site-packages\flask\app.py:1441(wsgi_app)
    6    0.000    0.000    0.000    0.000 C:\Python312\Lib\typing.py:1215(__setattr__)
    1    0.000    0.000    0.001    0.001 tracker\venv\Lib\site-packages\werkzeug\middleware\profiler.py:114(runapp)
  7/1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\routing\matcher.py:60(_update_state)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\wsgi.py:233(__init__)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\flask\app.py:1092(make_response)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\flask\app.py:867(full_dispatch_request)
    2    0.000    0.000    0.000    0.000 {method 'reset' of '_contextvars.ContextVar' objects}
    6    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\blinker\base.py:234(send)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\flask\ctx.py:367(push)
    1    0.000    0.000    0.000    0.000 C:\Python312\Lib\typing.py:1269(__init__)
   37    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\wrappers\response.py:547(get_wsgi_response)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\flask\app.py:1260(process_response)
    1    0.000    0.000    0.000    0.000 C:\Python312\Lib\typing.py:1560(__getitem_inner__)
    2    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\datastructures\headers.py:288(set)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\flask\app.py:885(finalize_request)
    4    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\local.py:310(__get__)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\wrappers\response.py:438(get_wsgi_headers)
    1    0.000    0.000    0.000    0.000 tracker\venv\Lib\site-packages\werkzeug\wrappers\response.py:144(__init__)
  9/8    0.000    0.000    0.000    0.000 {method 'encode' of 'str' objects}

--------------------------------------------------------------------------------

127.0.0.1 - - [05/Nov/2024 20:59:52] "GET / HTTP/1.1" 200 -
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
