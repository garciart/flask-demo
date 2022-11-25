# -*- coding: utf-8 -*-
"""Input validation module.

**WARNING** - DO NOT USE THE BUILT-IN validate.py! It accepts type Any for some inputs,
such as min_val (which should be int). This will lead to errors due to missing or incorrect
types or values, or offset arguments.
"""
__all__ = ['validate_integer',
           'validate_regex_match',
           'validate_type']

import re
import sre_constants
import sys


def validate_integer(input_val,
                     *,
                     min_val=0,
                     max_val=sys.maxsize,
                     err_msg='Invalid integer value.'):
    # type: (int, object, int, int, str) -> None
    """Verify an object is an integer and that it is not None or empty. Optionally,
    this method can verify the value of the number is greater or equal to a minimum,
    less than or equal to a maximum, or within a range in value.

    **NOTE:** - For upper value. Python type sizes are platform dependent,
    and are only limited by byte size, encoding, and amount of available memory.

    :param int input_val: The input to check
    :param int min_val: The desired minimum value of the input
    :param int max_val: The desired maximum value of the input
    :param str err_msg: A custom and generic error message, if desired
    :return: None
    :rtype: None
    :raise SyntaxError: If not all arguments are provided
    :raise ValueError: If an argument is invalid
    """
    # Validate types
    validate_type(input_val, int, err_msg='Input must be an integer.')
    validate_type(min_val, int, err_msg='Min value must be an integer.')
    validate_type(max_val, int, err_msg='Max value must be an integer.')
    # Check the values
    if not min_val <= input_val <= max_val:
        raise ValueError(err_msg)


def validate_regex_match(input_str,
                         pattern_str,
                         *,
                         err_msg='Regex does not match.'):
    # type: (str, str, object, str) -> None
    """Verify the input matches the regular expression pattern.

    **NOTE** - Do not submit a compiled pattern; submit a string.
    Cannot validate _sre.SRE_Pattern type.

    :param str input_str: The input to check
    :param str pattern_str: The non-compiled regular expression pattern to match as a string
    :param str err_msg: A custom and generic error message, if desired
    :return: None
    :rtype: None
    :raise SyntaxError: If not all arguments are provided
    :raise ValueError: If an argument is invalid
    """
    # Validate types
    # In Python 2.7, use str for ASCII and basestring for Unicode
    validate_type(input_str, str, err_msg='Input must be a string.')
    validate_type(pattern_str, str, err_msg='Pattern must be a string and not compiled.')
    # Verify the pattern is valid
    try:
        re.compile(pattern_str)
    except (ValueError, sre_constants.error):
        raise ValueError('Invalid pattern.')
    # Ensure the input matches the regex pattern
    if not bool(re.match(pattern_str, input_str)):
        raise ValueError(err_msg)


def validate_type(input_obj,
                  obj_type,
                  *,
                  err_msg='Types do not match.'):
    # type: (object, (type, tuple), object, str) -> None
    """Verify the input is the correct type. Can be used to verify str, int, etc.

    **NOTE** - This method does not use isinstance() to validate object type,
    to prevent validating True and False as int 1 and 0, or basestring as str.
    However, this method will still validate byte strings as strings.

    **NOTE** - This method only validates the type is correct;
    it does not check for empty strings and strings containing only newline characters.

    :param object input_obj: The input to check
    :param type or tuple obj_type: The expected type
    :param str err_msg: A custom and generic error message, if desired
    :return: None
    :rtype: None
    :raise SyntaxError: If not all arguments are provided
    :raise ValueError: If an argument is invalid
    """
    # Wrap single obj_type argument in a tuple
    if not isinstance(obj_type, tuple):
        obj_type = (obj_type,)
    # Compare the value to the type
    if type(input_obj) not in obj_type:
        raise ValueError(err_msg)
