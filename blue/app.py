"""Starting point for the Blue application.

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Usage:

- `python -B app.py`
- `python -B -m flask --app "app" run`
- `python -B -m flask --app "app" run --debug  # Allow hot reloads`
- `python -B -m flask run  # Flask will look in 'app.py' or in the 'app' directory if the '--app' option is missing`
- `python -B -m flask run --host=0.0.0.0  # Allow outside access in NO DEBUG mode`
"""

import app

if __name__ == '__main__':
    _app = app.create_app()
    _app.run()
