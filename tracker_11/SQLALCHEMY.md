```shell
# Check the application for issues
python -B -m pylint tracker_11
# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest discover tracker_11/tests -b -v
# See the coverage report in the console
coverage report -m
# Initialize migration support for the application
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_11 db init --directory tracker_11/migrations
python -B -m flask --app tracker_11 db init -d tracker_11/migrations
# Perform an initial migration to capture the current schema of the database
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_11 db migrate --message "Initial migration" --directory tracker_11/migrations
python -B -m flask --app tracker_11 db migrate -m "Initial migration" -d tracker_11/migrations
# For help with any of these commands, use python -B -m flask --app tracker_11 db --help


# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_11:create_app('profiler')" run --without-threads
# Create a log when running the Flask application
# python -B -m flask --app "tracker_11:create_app(config_name='development', log_events=True)" run
python -B -m flask --app "tracker_11:create_app('development', True)" run
```