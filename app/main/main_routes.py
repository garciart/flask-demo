"""Main content routing manager.

TODO: Replace role_id with a privilege level system!

Test: http://127.0.0.1:5000
"""
# Flake8 F401: imports are used for type hints
from flask import (abort, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.main_forms import SimpleForm
from app.models import User, Course, Role, Association

_DUMMY_DATA = [
    {'course_id': 1, 'course_name': 'Python 101', 'course_code': 'CS100',
     'course_group': 'SDEV', 'course_desc': 'Introduction to Python.',
     'role_name': 'Teacher'},
    {'course_id': 2, 'course_name': 'Flask 101', 'course_code': 'CS101',
     'course_group': 'SDEV', 'course_desc': 'Introduction to Flask.',
     'role_name': 'Student'}
]

INDEX_PAGE = 'main.index'
LOGIN_REQ_MSG = 'You must log in.'


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # type: () -> str
    """The landing page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Flask Demo'

    if current_user.is_admin:
        _courses = Course.query.all()
    else:
        _user_id = int(current_user.get_id())

        _courses = db.session.query(
            Course.course_id, Course.course_name, Course.course_code,
            Course.course_group, Course.course_desc,
            Role.role_id, Role.role_name).join(
                Association,
                Course.course_id == Association.course_id).join(
                    Role, Role.role_id == Association.role_id).filter(
                        Association.user_id == _user_id).all()

    # Convert to list if there is only one result
    _courses = [_courses] if not isinstance(_courses, list) else _courses

    # Send the list to the page
    _html = render_template('main/index.html', page_title=_page_title,
                            courses=_courses)
    return _html


@bp.route('/about')
def about():
    # type: () -> str
    """The about page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'About'
    _html = render_template('main/about.html', page_title=_page_title)
    return _html


@bp.route('/courses')
@login_required
def courses():
    # type: () -> str
    """The course list page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    # Redirect if not an Administrator
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'List of Courses'

    _courses = Course.query.all()

    # Convert to list if there is only one result
    _courses = [_courses] if not isinstance(_courses, list) else _courses

    _html = render_template('main/courses.html', page_title=_page_title,
                            courses=_courses)
    return _html


@bp.route('/roles')
@login_required
def roles():
    # type: () -> str
    """The role list page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    # An alternate way of preventing non-admins from accessing page
    if not current_user.is_admin:
        _roles = Role.query.get_or_404(current_user.get_id(),
                                       LOGIN_REQ_MSG)
    else:
        _roles = Role.query.all()

    _page_title = 'List of Roles'

    # Convert to list if there is only one result
    _roles = [_roles] if not isinstance(_roles, list) else _roles

    _html = render_template('main/roles.html', page_title=_page_title,
                            roles=_roles)
    return _html


@bp.route('/users')
@login_required
def users():
    # type: () -> str
    """The user list page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    # Redirect if not an Administrator
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'List of Users'

    _users = User.query.all()

    # Convert to list if there is only one result
    _users = [_users] if not isinstance(_users, list) else _users

    _html = render_template('main/users.html', page_title=_page_title,
                            users=_users)
    return _html


@bp.route('/test')
@login_required
def test():
    # type: () -> str
    """Test page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Flask Demo'

    _courses = _DUMMY_DATA

    _html = render_template('main/index.html', page_title=_page_title,
                            courses=_courses)
    return _html


@bp.route('/scratch/<int:course_id>', methods=['GET', 'POST'])
@login_required
def scratch(course_id):
    # type: (int) -> str
    """Scratch page.

    :param int course_id: The ID of the course to modify access

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    # Redirect if not an Administrator
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    # Set the page title
    _page_title = 'Assign Users to Course'

    # Instantiate the form
    _form = SimpleForm()
    
    # Get the course data from the database
    _course = Course.query.get_or_404(course_id)

    # Get a list of roles from the database
    _roles = Role.query.all()
    
    # Ensure the result is a list so you can iterate through it
    # (One result is a Role object, and you can't iterate Role)
    _roles = [_roles] if not isinstance(_roles, list) else _roles

    # print('_roles', _roles, type(_roles))
    # print('_roles[2]', _roles[2], type(_roles[2]))

    # Create a list to hold role information
    # You will iterate through this list of dictionaries,
    # instead of a list of Role objects, when you render the webpage
    _roles_list = []

    for _r in _roles:
        _role_dict = _r.__dict__

        # print("_role_dict", _role_dict, type(_role_dict))
        # print("_role_dict['role_name']", _role_dict['role_name'],
        # type(_role_dict['role_name']))
        
        _roles_list.append(_role_dict)
    
    _roles_list.append({"role_id": 4, "role_name": "Not Assigned"})
    
    # print("_roles_list", _roles_list, type(_roles_list))
    # print("_roles_list[3]", _roles_list[3], type(_roles_list[3]))
    # print("_roles_list[3]['role_name']", _roles_list[3]['role_name'],
    # type(_roles_list[3]['role_name']))

    # Get a list of users by name from the database
    _users = User.query.order_by(User.username).all()
    
    # Ensure the result is a list so you can iterate through it
    _users = [_users] if not isinstance(_users, list) else _users
    
    # print('_users', _users, type(_users))
    # print('_users[3]', _users[3], type(_users[3]))

    # Create a list to hold user information
    # You will iterate through this list of dictionaries,
    # instead of a list of User objects, when you render the webpage
    _users_list = []

    for _u in _users:
        _user_dict = _u.__dict__
        _user_dict['role_id'] = 4
        _a = Association.query.filter(
            Association.course_id == course_id,
            Association.user_id == _user_dict['user_id']).first()

        # print("_a", _a, type(_a))

        if _a is not None:
            _user_dict['role_id'] = _a.role_id

        # print("_user_dict", _user_dict, type(_user_dict))
        # print("_user_dict['username']", _user_dict['username'],
        # type(_user_dict['username']))
        
        _users_list.append(_user_dict)

    # print("_users_list", _users_list, type(_users_list))
    # print("_users_list[0]", _users_list[0], type(_users_list[0]))
    # print("_users_list[0]['username']", _users_list[0]['username'],
    # type(_users_list[0]['username']))

    if request.method == 'GET':
        return render_template(
            'main/scratch.html',
            page_title=_page_title,
            course_name=_course.course_name,
            form=_form,
            roles=_roles_list,
            users_list=_users_list)
    elif request.method == 'POST':
        flash(request.form.getlist('14'))
        # for _u in _users_list:
        #     _id = str(_u['user_id'])
        #     _o = request.form[_id]
            # flash(f"{_u['username']} {_u['user_id']}")

        return redirect(url_for(INDEX_PAGE))
    else:
        print('Oh.')
        abort(500)
