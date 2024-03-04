"""API routing manager.

Test: http://127.0.0.1:5000/api/test
"""
# Flake8 F401: imports are used for type hints
from flask import (jsonify, Response)  # noqa: F401
from app.api import api_bp
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

    # Optional: Only include key-value pairs whose key is in the list of fields
    _fields = ['course_id', 'course_name', 'course_code', 'course_group']

    _json_result = __serialize_query_result(_courses, _fields)
    # _json_result = __serialize_query_result(_courses)

    return _json_result


def __serialize_query_result(db_object, fields=None):
    # type: (object, list) -> list
    """Serialize SQLAlchemy query result.

    query_all() returns a list of class objects,
    formatted using the class's __repr__ method.

    You need to convert those class objects to dict objects
    before displaying as json.

    NOTE - jsonify, json.loads and json.dump do not work

    :param object db_object: The SQLAlchemy query result
    :param list fields: Only include key-value pairs whose key is in the
    list of fields, defaults to [] for all fields

    :return: The serialized result
    :rtype: list
    """
    # Holds the converted objects
    _converted_list = []

    # _o: object, _k: key, _v: value
    for _o in db_object:
        if fields is None:
            _filtered_dict = dict(_o.__dict__.items())
        else:
            _filtered_dict = {
                _k: _v for _k, _v in _o.__dict__.items() if _k in fields}

        # Remove SQLAlchemy internal objects
        if '_sa_instance_state' in _filtered_dict:
            del _filtered_dict['_sa_instance_state']

        _converted_list.append(_filtered_dict)

    return _converted_list
