# code: language=ini
# Environment variables for this app for python-dotenv

# The file or package that you will use to create the Flask application instance and define routes.
# The defaults are the 'app.py' file and the 'app' package
FLASK_APP=app

# The environment you want to use, like 'development', 'testing', or 'production'.
# If you set the environment to 'development', Flask automatically enables Debug mode.
FLASK_ENV=development
# Allow Flask to reload your application if it detects changes to the Python code or imported modules.
FLASK_DEBUG=false
# Allow Flask to reload your application if it detects changes to the listed files.
FLASK_RUN_EXTRA_FILES=

# The certificate file to use when running the app using the HTTPS protocol.
FLASK_RUN_CERT=
# The key file for the HTTPS certificate.
FLASK_RUN_KEY=

# The IP address or hostname you want to bind your app to. The default is '127.0.0.1'.
FLASK_RUN_HOST="127.0.0.1"
# The port you want to use. The default is 5000.
FLASK_RUN_PORT=5000
# The key Flask will use to protect your app from Cross-site request forgery (CRSF) attacks
SECRET_KEY='The CRSF protection key you would set in your OS environment would go here.'
