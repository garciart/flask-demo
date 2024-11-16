"""API routing manager.

Test: http://127.0.0.1:5000/api/test
"""
# Flake8 F401: imports are used for type hints
from flask import (jsonify, Response)
from app.api import api_bp
from app.app_utils import validate_input
from app.models import Course

_DUMMY_DATA = [
    {'course_id': 1, 'course_name': 'Python 101', 'course_code': 'CS100',
     'course_group': 'SDEV', 'course_desc': 'Introduction to Python.',
     'role_name': 'Teacher'},
    {'course_id': 2, 'course_name': 'Flask 101', 'course_code': 'CS101',
     'course_group': 'SDEV', 'course_desc': 'Introduction to Flask.',
     'role_name': 'Student'}
]


@api_bp.route('/api/test', methods=['GET'])
def get_test_data():
    # type: () -> Response
    """Get the list of test data when a REST call is made.

    :returns: A response with the data in JSON format
    :rtype: Response
    """
    _response = jsonify(test_data=_DUMMY_DATA, status=200,
                        mimetype='application/json')
    return _response


@api_bp.route('/api/courses', methods=['GET'])
def api_courses():
    # type: () -> Response
    """Get the list of courses in the database when a REST call is made.

    :returns: A response with the data in JSON format
    :rtype: Response
    """
    _courses = Course.query.all()

    _exclude = ['course_code']

    _json_result = __serialize_query_result(_courses, _exclude)
    # _json_result = __serialize_query_result(_courses)

    return _json_result


def __serialize_query_result(query_result: list, exclude: None | str | list = None) -> list:
    """Serialize SQLAlchemy query result into a JSON string.

    NOTE - Do not tinker! This works and you wasted three hours on this

    NOTE - defer, load_only, etc., do not work

    <model class>.query.one() returns a single model object,
    formatted using the __repr__ method of the model.

    <model class>.query.all() returns a list of model objects,
    formatted using the __repr__ method of the model.

    You need to convert those model objects to dict objects before displaying as json.

    :param list query_result: The SQLAlchemy query result as a list of model objects, like [Member],
        or none
    :param str/list exclude: Key(s)/Column(s) to remove from results

    :returns: The serialized result
    :rtype: list
    """
    # Validate inputs
    validate_input('query_result', query_result, list)
    validate_input('exclude', exclude, (None | str | list))

    # Holds the converted objects
    _converted_list = []

    # _o = class object, _k = key, and _v = value
    for _o in query_result:
        if exclude is None:
            _filtered_dict = dict(_o.__dict__.items())
        else:
            _filtered_dict = {
                _k: _v for _k, _v in _o.__dict__.items() if _k not in exclude}

        # Remove SQLAlchemy internal objects
        if '_sa_instance_state' in _filtered_dict:
            del _filtered_dict['_sa_instance_state']

        _converted_list.append(_filtered_dict)

    return _converted_list