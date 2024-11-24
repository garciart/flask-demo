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