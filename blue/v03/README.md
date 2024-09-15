# Blue v03

This is an example of passing and using different configuration options with a Flask application.

Usage:

- `python -B -m flask --app "v03" run`
- `python -B -m flask --app "v03:create_app(config_class='v03.config.DevConfig')" run`
- `python -B -m flask --app "v03:create_app(config_class='v03.config.TestConfig')" run`
