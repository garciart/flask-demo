```shell
# Check the application for issues
python -B -m pylint tracker_09
# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest discover tracker_09/tests -b -v
# See the coverage report in the console
coverage report -m
# Initialize migration support for the application
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_09 db init --directory tracker_09/migrations
python -B -m flask --app tracker_09 db init -d tracker_09/migrations
# Perform an initial migration to capture the current schema of the database
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_09 db migrate --message "Initial migration" --directory tracker_09/migrations
python -B -m flask --app tracker_09 db migrate -m "Initial migration" -d tracker_09/migrations
# For help with any of these commands, use python -B -m flask --app tracker_09 db --help


# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_09:create_app('profiler')" run --without-threads
# Create a log when running the Flask application
# python -B -m flask --app "tracker_09:create_app(config_name='development', log_events=True)" run
python -B -m flask --app "tracker_09:create_app('development', True)" run
```
