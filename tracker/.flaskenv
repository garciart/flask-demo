# code: language=ini
# Flask environment variables for this app (loaded by python-dotenv)

# Do not use FLASK_ENV (since 2.2.0):
# "The FLASK_ENV environment variable and app.env attribute are deprecated,
# removing the distinction between development and debug mode.
# Debug mode should be controlled directly using the --debug option or app.run(debug=True)."
# .. seealso:: https://flask.palletsprojects.com/en/stable/changes/
# If neccessary, use FLASK_DEBUG instead to allow Flask to reload your application
# if it detects changes to the Python code or imported modules.
# FLASK_DEBUG=true

# Allow Flask to reload your application if it detects changes to the listed files.
# FLASK_RUN_EXTRA_FILES=

# Flask will use this certificate file when running the app using the HTTPS protocol.
# FLASK_RUN_CERT=

# Flask will use this key file for the HTTPS certificate.
# FLASK_RUN_KEY=

# Flask will bind your app to this IP address or hostname. The default is '127.0.0.1'.
# FLASK_RUN_HOST="127.0.0.1"

# Flask will use this port. The default is 5000.
# FLASK_RUN_PORT=5000

# Flask will use this key to protect your app from Cross-site request forgery (CRSF) attacks
# SECRET_KEY='abcdef01234567899876543210fedcbaabcdef01234567899876543210fedcba'

# User-defined Flask environment variable
FLASKENV_USER_DEFINED_VAR="fedcba9876543210"