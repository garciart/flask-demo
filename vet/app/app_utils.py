"""Helper functions
"""
import inspect
from types import FrameType, UnionType
from flask import (abort, current_app)


def validate_input(obj_name, obj_to_check, expected_type):
    # type: (str, object, type | tuple | UnionType) -> None
    """Validate an input's type and ensure it is not empty.

    Use this function to reduce code complexity in calling functions and methods.

    :param str obj_name: The name of the input to validate
    :param object obj_to_check: The input to validate
    :param type/tuple/UnionType expected_type: The expected type or list of types for the input

    :returns: None
    :rtype: None
    """
    # Validate inputs for this function
    _current_function = inspect.currentframe()

    if not isinstance(obj_name, str):
        _error_msg = 'obj_name must be type <str>.'
        _log_error_and_exit(_error_msg, _current_function)

    if not isinstance(expected_type, type):
        _error_msg = 'expected_type must be type <type>.'
        _log_error_and_exit(_error_msg, _current_function)

    # Validate inputs for the calling function
    _calling_function = inspect.currentframe().f_back

    if not isinstance(obj_to_check, expected_type):
        _error_msg = f"'{obj_name}' is not type {expected_type}."
        _log_error_and_exit(_error_msg, _calling_function)

    if isinstance(obj_to_check, str) and obj_to_check == '':
        _error_msg = f"'{obj_name}' is empty."
        _log_error_and_exit(_error_msg, _calling_function)

    if isinstance(obj_to_check, (str, list, dict)) and len(obj_to_check) == 0:
        _error_msg = f"'{obj_name}' is empty."
        _log_error_and_exit(_error_msg, _calling_function)


def _log_error_and_exit(error_msg, calling_function=None):
    # type: (str, FrameType) -> None
    """Provide the location of the error and a message

    :param str error_msg: A custom error message
    :param types.FrameType calling_function: An object containing stack
        information (e.g., where the error occurred), defaults to None. If not
        provided, this function will use the stack of the previous function

    :returns: None
    :rtype: None
    """
    # Validate inputs
    if not isinstance(error_msg, str):
        current_app.logger.error('obj_name must be type <str>.')
        abort(500)

    if calling_function is not None and not isinstance(calling_function,
                                                       FrameType):
        current_app.logger.error(
            'expected_type must be type <types.FrameType>.')
        abort(500)

    if calling_function is None:
        calling_function = inspect.currentframe().f_back

    # Get path, method, and line number where the error occurred
    _msg = (f'>>> Error: {error_msg} '
            f'(see {calling_function.f_code.co_filename}, '
            f'{calling_function.f_code.co_name}(), '
            f'line {calling_function.f_lineno}).')
    current_app.logger.critical(_msg)
    abort(500)
