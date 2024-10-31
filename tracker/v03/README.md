# Tracker v03

Use different environment, Flask, and application configuration options.

Usage:

- `python -B -m flask --app "v03" run`
- `python -B -m flask --app "v03:create_app(config_class='v03.config.DevConfig')" run`
- `python -B -m flask --app "v03:create_app(config_class='v03.config.TestConfig')" run`
