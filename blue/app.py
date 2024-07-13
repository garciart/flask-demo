"""Starting point for the Blue application.

Python options
-B     : don't write .pyc files on import; also PYTHONDONTWRITEBYTECODE=x
-m mod : run library module as a script (terminates option list)

Usage:
- python -B -m flask run
- python -B -m flask --app blue_app run
- python -B -m flask --app blue_app run --debug  # Allow hot reloads
- python -B -m flask run --host=0.0.0.0  # Allow outside access in NO DEBUG mode
"""
import argparse

parser = argparse.ArgumentParser(
    description='Blue App',
    epilog='To run: python -m flask run')
args, _ = parser.parse_known_args()
