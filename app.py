"""Flask Template.

Usage:
- python3 -m flask run
- python3 -m flask --app app run
- python3 -m flask --app app run --debug  # Allow hot reloads
- python3 -m flask run --host=0.0.0.0  # Allow outside access in NO DEBUG mode
"""
import argparse

parser = argparse.ArgumentParser(
    description='Flask Template',
    epilog='To run: python3 -m flask run')
args, _ = parser.parse_known_args()
