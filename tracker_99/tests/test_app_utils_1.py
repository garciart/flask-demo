"""Test methods and functions in app_utils.py

Run with -s option to allow tests to use the 'print' command within the tests
to display messages along with pylint output (i.e., `pytest tracker_99/tests -s` or
`coverage run -m pytest tracker_99/tests -s`)
"""

import importlib
import sys

from tracker_99.app_utils import check_system

# Get the Python version number and convert it to float (e.g., 3.9 -> 3.09)
SYS_PYTHON_VERSION = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

# Get the Flask major and minor version numbers and convert them to a float
raw_flask_version = importlib.metadata.version("flask")
flask_version_major, flask_version_minor = map(int, raw_flask_version.split('.')[:2])
SYS_FLASK_VERSION = float(f"{flask_version_major}.{flask_version_minor:02d}")


def test_check_system_pass_meets_req():
    """Test that check_system() passes when requirements met"""
    check_system(min_python_version=SYS_PYTHON_VERSION, min_flask_version=SYS_FLASK_VERSION)


def test_check_system_pass_exceeds_req():
    """Test that check_system() passes when requirements exceeded"""
    check_system(
        # Temporarily lower the required versions to test (i.e., 3.12 - 0.1 = 3.02)
        min_python_version=SYS_PYTHON_VERSION - 0.1,
        min_flask_version=SYS_FLASK_VERSION - 0.1,
    )
