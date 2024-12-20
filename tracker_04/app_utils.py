"""Helper functions
"""

import importlib
import sys
from types import UnionType

__all__ = ['check_system', 'validate_input']

from typing import Union


def check_system(min_python_version: float = 3.08, min_flask_version: float = 3.0) -> tuple:
    """Check if the installed Python and Flask versions can run the application.

    **NOTE** - Use `3.01` for version `3.1` and `3.10` for version `3.10`.

    :param float min_python_version: The minimum Python version in float format, defaults to 3.08
    :param float min_flask_version: The minimum Flask version in float format, defaults to 3.0

    :returns: The Python and Flask versions in float format (`3.01` for version `3.1`, etc.)
    :rtype: tuple
    """
    # Validate inputs
    validate_input('min_python_version', min_python_version, float)
    validate_input('min_flask_version', min_python_version, float)

    if min_python_version <= 0.0 or min_flask_version <= 0.0:
        raise ValueError(
            'The minimum Python and Flask version numbers must be greater than 0. Exiting now...'
        )

    # Get the Python version number and convert it to float (e.g., 3.9 -> 3.09)
    _python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

    # Ensure you are using the correct version of Python
    print(f"Your Python version is {_python_version}.")
    if _python_version < min_python_version:
        raise ValueError(
            f"Flask 3 requires Python {min_python_version:.2f} or above. Exiting now..."
        )

    # Get the Flask major and minor version numbers and convert them to a float
    _raw_flask_version = importlib.metadata.version("flask")
    _flask_version_major, _flask_version_minor = map(int, _raw_flask_version.split('.')[:2])
    _flask_version = float(f"{_flask_version_major}.{_flask_version_minor:02d}")

    # Ensure you are using the correct version of Flask
    print(f"Your Flask version is {_raw_flask_version}.")
    if float(_flask_version) < min_flask_version:
        raise ValueError(
            f"This application requires Flask {min_flask_version:.2f} or above. Exiting now..."
        )

    return _python_version, _flask_version


def validate_input(
    obj_name: str, obj_to_check: object, expected_type: Union[type, tuple, UnionType]
) -> None:
    """Validate an input's type and ensure it is not empty.

    Use this function to reduce code complexity in calling functions and methods.

    :param str obj_name: The name of the input to validate
    :param object obj_to_check: The input to validate
    :param type/tuple/UnionType expected_type: The expected type or list of types for the input

    :returns None: None
    """
    if not isinstance(obj_to_check, expected_type):
        raise TypeError(f"'{obj_name}' is not type {expected_type}. Exiting now...")

    if isinstance(obj_to_check, (str, list, dict)) and len(obj_to_check) == 0:
        raise ValueError(f"'{obj_name}' is empty. Exiting now...")
