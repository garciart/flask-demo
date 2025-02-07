# Miscellaneous

```shell
# Apply any pending migrations to the database.
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_09 db upgrade --directory tracker_09/migrations
python -B -m flask --app tracker_09 db upgrade -d tracker_09/migrations
```

In addition, you may eventually need to modify your database, like when you need to add columns, etc. To "transfer" your data to your new schema without losing data, you perform a database *migration*. To reduce the chances of issues with future migrations, perform an initial migration before you run the application:

```shell
# Check the application for issues
python -B -m pylint tracker_09
# Initialize migration support for the application
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_09 db init --directory tracker_09/migrations
python -B -m flask --app tracker_09 db init -d tracker_09/migrations
# Perform an initial migration to capture the current schema of the database
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_09 db migrate --message "Initial migration" --directory tracker_09/migrations
python -B -m flask --app tracker_09 db migrate -m "Initial migration" -d tracker_09/migrations
# Apply any pending migrations to the database.
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_09 db upgrade --directory tracker_09/migrations
python -B -m flask --app tracker_09 db upgrade -d tracker_09/migrations
# For help with any of these commands, use python -B -m flask --app tracker_09 db --help
```

That will create a `migrations` directory in your package (`tracker_09`) directory.


## Background

Python Enhancement Proposals (PEP) 333 and 3333, the Python Web Server Gateway Interface (WSGI), is a specification that defines how a web server communicates with a Python web application or framework. It acts as a bridge between them, increasing portability and allowing you to run Python applications on different web servers with ease.
Flask is a WSGI application.
It has a built-in Werkzeug server that converts incoming HTTP requests (GET, POST, etc.)

The Python Web Server Gateway Interface (WSGI) is a specification that defines a standard interface between web servers and Python web applications or frameworks. It acts as a bridge, allowing different web servers to communicate with different Python applications seamlessly.
Here's a breakdown of WSGI:
Components:
Web Server:
The software that handles incoming HTTP requests from clients (e.g., Apache, Nginx).
WSGI Server:
A component that implements the WSGI specification and interacts with the web server (e.g., Gunicorn, uWSGI).
WSGI Application:
Your Python web application or framework (e.g., Flask, Django) that adheres to the WSGI specification.
How it Works:
The web server receives an HTTP request from a client.
The web server forwards the request to the WSGI server.
The WSGI server calls a specific callable object (usually a function) within your WSGI application.
Your application processes the request, generates a response, and returns it to the WSGI server.
The WSGI server converts the response to an HTTP response and sends it back to the web server.
The web server delivers the response to the client.
Benefits of WSGI:
Portability:
You can easily switch between different web servers and frameworks without modifying your application code.
Flexibility:
WSGI allows you to build complex web applications by chaining multiple WSGI applications together (middleware).
Scalability:
WSGI servers like Gunicorn and uWSGI provide advanced features for handling multiple requests concurrently, improving the performance of your application.

-----

## Best Practices

Use a virtual environment
Change maximum line length to 100 characters
Use PEP-8 naming conventions
Write docstrings per PEP 257 using reStructuredText style.
Include "Usage:" comments in the header docstring of modules
Include type hints when defining the parameters of an function or method
Pass keyword arguments instead of depending on positional parsing
Consolidate repeated code into functions or methods (DRY)
Organize related code and modules into packages
Use relative imports; check them after any changes!
Stick to the Standard Library when possible
Use input validation
Do not hard code sensitive information
Use parentheses instead of slashes for long line continuations
Use simple and readable code instead of LEET code
Use comments often

Include logging module
Include profiling to find bottlenecks


Lint code with PyLint after making any changes
Add, update, and run unit tests for edge cases with unittest after making any changes
Run application using the 'development' configuration first and check the logs
Do not log when running the application in hotfix or 'debug' mode

