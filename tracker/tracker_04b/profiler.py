from werkzeug.middleware.profiler import ProfilerMiddleware


def add_profiler_middleware(app):
    # Add ProfilerMiddleware to your Flask app.
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    return app
