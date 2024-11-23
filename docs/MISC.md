# Miscellaneous

```shell
# Apply any pending migrations to the database.
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_09 db upgrade --directory tracker_09/migrations
python -B -m flask --app tracker_09 db upgrade -d tracker_09/migrations
```
