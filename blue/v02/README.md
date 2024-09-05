# Blue v02

This is an example of passing and using different configuration options with a Flask application.

Usage:

- `python -B -m flask --app "v02" run`
- `python -B -m flask --app "v02:create_app(config_class='v02.config.DevConfig')" run`
- `python -B -m flask --app "v02:create_app(config_class='v02.config.TestConfig')" run`
