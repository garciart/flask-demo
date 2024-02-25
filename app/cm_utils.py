"""Helper functions
"""
import inspect
import sys
from types import FrameType
from app import app


def validate_inputs(obj_name, obj_to_check, expected_type):
    # type: (str, object, type) -> None
    """Validate an input's type and ensure it is not empty. Use this
    function to reduce code complexity in calling functions and methods.

    :param str obj_name: The name of the input to validate
    :param object obj_to_check: The input to validate
    :param type expected_type: The expected type for the input

    :returns: None
    """
    # Validate inputs
    if not isinstance(obj_name, str):
        raise TypeError('obj_name must be type <str>.')

    if not isinstance(expected_type, type):
        raise TypeError('expected_type must be type <type>.')

    _calling_method = inspect.currentframe().f_back

    if not isinstance(obj_to_check, expected_type):
        _error_msg = f"'{obj_name}' is not type {expected_type}."
        _log_error_and_exit(_error_msg, _calling_method)

    if isinstance(obj_to_check, str) and obj_to_check == '':
        _error_msg = f"'{obj_name}' is empty."
        _log_error_and_exit(_error_msg, _calling_method)

    if isinstance(obj_to_check, (str, list, dict)) and len(obj_to_check) == 0:
        _error_msg = f"'{obj_name}' is empty."
        _log_error_and_exit(_error_msg, _calling_method)


def _log_error_and_exit(error_msg, calling_method=None):
    # type: (str, FrameType) -> None
    """Provide the location of the error and a message

    :param str error_msg: A custom error message
    :param types.FrameType calling_method: An object containing stack
        information (e.g., where the error occurred), defaults to None. If not
        provided, this function will use the stack of the previous function
    :returns: None
    """
    # Validate inputs
    if not isinstance(error_msg, str):
        raise TypeError('obj_name must be type <str>.')

    if calling_method is not None and not isinstance(calling_method,
                                                     FrameType):
        raise TypeError('expected_type must be type <types.FrameType>.')

    if calling_method is None:
        calling_method = inspect.currentframe().f_back

    _msg = (f'>>> Error: {error_msg} (see {calling_method.f_code.co_name}(), '
            f'line {calling_method.f_lineno}).')
    app.logger.critical(_msg)
    print('Exiting now...')
    sys.exit(1)
