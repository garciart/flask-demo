"""Course Administration Routing Manager.
"""

from typing import Union

from flask import Response, abort, flash, redirect, url_for, render_template, request
from flask_login import current_user, login_required

from tracker_99 import db, constants as c
from tracker_99.app_utils import validate_input
from tracker_99.blueprints.admin import admin_bp
from tracker_99.blueprints.admin.course_forms import (
    AddCourseForm,
    EditCourseForm,
    DeleteCourseForm,
)
from tracker_99.models.models import Course, Association, Member, Role


# Allow `except Exception as e` so issues can percolate up, like ValueErrors from the model
# pylint: disable=broad-except


@admin_bp.route('/admin/add_course', methods=['GET', 'POST'])
@login_required
def add_course() -> Union[str, Response]:
    """Use form input to add a course in the database.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    _page_title = 'Add Course'
    _page_description = 'Add Course'

    _form = AddCourseForm()

    if _form.validate_on_submit():
        try:
            # Instantiate a Course object
            _course = Course(
                course_name=_form.course_name.data,
                course_code=_form.course_code.data,
                course_group=_form.course_group.data,
                course_desc=_form.course_desc.data,
            )
            # Use the setter in the Course class to set Course.course_key
            _course.set_key(_form.course_key.data)
            """
            INSERT INTO courses (course_name, course_code, course_group, course_key, course_desc)
            VALUES ("Building Bad Python Applications", "SDEV 301", "SDEV",
                b'\xe1<\x9c\x01~\xd0_S\x8fR\xf8\x92W\x80|\xc1AAJ\xeb\xd8\xf3\xa4f\xd4&%1\r\xe7\xfaI\x1eO5\xa0\xa1\x9f\x99W\xab',
                "Not recommended!");
            """
            db.session.add(_course)
            db.session.commit()

            # Get row_id of the new course
            _new_id = _course.course_id

            # Get the first role_id that has owner privileges
            # instead of using a hard-coded int or ID
            """
            SELECT roles.role_id
            FROM roles
            WHERE roles.role_privilege = 30
            LIMIT 1;
            """
            _role_id = (db.session.query(Role.role_id)
                .filter(Role.role_privilege == 30)
                .limit(1)
                .scalar())

            # Add the course and chair to the association table
            _member_id = int(current_user.get_id())
            _assoc = Association(course_id=_new_id, role_id=_role_id, member_id=_member_id)

            db.session.add(_assoc)
            db.session.commit()

            flash('Addition successful.')
            return redirect(url_for(c.COURSES_PAGE))
        # except exc.IntegrityError:
        #     db.session.rollback()
        #     flash('Addition failed: Course exists', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Addition failed: {str(e)}', 'error')

    # Default behavior if not sending data to the server (POST, etc.)
    # Re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'add_course.html',
        page_title=_page_title,
        page_description=_page_description,
        form=_form,
    )


@admin_bp.route('/admin/view_course/<int:course_id>', methods=['GET'])
@login_required
def view_course(course_id: int) -> Union[str, Response]:
    """View a course in the database.

    :param int course_id: The course to retrieve by ID

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('course_id', course_id, int)

    # Ensure the current user can view the course
    if _get_privilege_level(course_id=course_id) < 1:
        abort(403, c.NOT_AUTH_MSG)

    _page_title = 'View Course'
    _page_description = 'View Course'

    # Verify course exists
    """
    SELECT * FROM courses WHERE course_id = 17;
    """
    _course = Course.query.get_or_404(course_id)

    # Use a new variable since SQLAlchemy keeps track of objects and their attributes,
    # and redefining _course.course_key will cause an error
    _decrypted_key = Course.decrypt_text(_course.course_key)

    # Get a list of chairs to show to the viewer
    """
    SELECT members.member_name
    FROM courses,
        members,
        associations,
        roles
    WHERE courses.course_id = 3 AND
        roles.role_privilege >= 30 AND
        courses.course_id = associations.course_id AND
        members.member_id = associations.member_id AND
        roles.role_id = associations.role_id;
    """
    _chairs = (db.session.query(Member.member_name)
        .join(Association, Association.member_id == Member.member_id)
        .join(Course, Course.course_id == Association.course_id)
        .join(Role, Role.role_id == Association.role_id)
        .filter(Course.course_id == course_id,
                Role.role_privilege >= c.PRIVILEGE_LVL_OWNER)
        .all())

    # Convert list of one-item tuples [('liet.kynes',)] to a list of str ['liet.kynes']
    _chairs = [item[0] for item in _chairs]

    return render_template(
        'view_course.html',
        page_title=_page_title,
        page_description=_page_description,
        course=_course,
        decrypted_key=_decrypted_key,
        chairs=_chairs
    )


@admin_bp.route('/admin/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id: int) -> Union[str, Response]:
    """Use form input to update a course in the database.

    :param int course_id: The course to edit by ID

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('course_id', course_id, int)

    # Ensure the current user can view the course
    if _get_privilege_level(course_id=course_id) < c.PRIVILEGE_LVL_EDITOR:
        abort(403, c.NOT_AUTH_MSG)

    _page_title = 'Edit Course'
    _page_description = 'Edit Course'

    # Verify course exists
    """
    SELECT * FROM courses WHERE course_id = 17;
    """
    _course = Course.query.get_or_404(course_id)

    # Pass the current course name and code to check for duplicates
    _form = EditCourseForm(_course.course_name, _course.course_code)

    # Pre-populate form with current course details
    if request.method == 'GET':
        _form.course_name.data = _course.course_name
        _form.course_code.data = _course.course_code
        _form.course_group.data = _course.course_group
        _form.course_desc.data = _course.course_desc

    if _form.validate_on_submit():
        try:
            _course.course_name = _form.course_name.data
            _course.course_code = _form.course_code.data
            _course.course_group = _form.course_group.data
            # Only update the password if data was entered in the password fields
            if _form.course_key.data.strip() != '':
                # Use the setter in the Course class to set Course.course_key
                _course.set_key(_form.course_key.data)
            _course.course_desc = _form.course_desc.data
            """
            UPDATE courses
            SET course_name = "Building Better Python Applications",
                course_code = "SDEV 305",
                course_group = "SDEV",
                course_key = b'\xe1<\x9c\x01~\xd0_S\x8fR\xf8\x92W\x80|\xc1AAJ\xeb\xd8\xf3\xa4f\xd4&%1\r\xe7\xfaI\x1eO5\xa0\xa1\x9f\x99W\xab'
                course_desc = "Better than before!"
            WHERE course_id = 17;
            """
            # db.session.add(_course)
            db.session.commit()
            flash('Update successful.')
            return redirect(url_for(c.COURSES_PAGE))
        # except exc.IntegrityError:
        #     db.session.rollback()
        #     flash('Update failed: Course exists', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Update failed: {str(e)}', 'error')

    # Default behavior if not sending data to the server (POST, etc.)
    # Re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'edit_course.html',
        page_title=_page_title,
        page_description=_page_description,
        form=_form,
    )


@admin_bp.route('/admin/delete_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def delete_course(course_id: int) -> Union[str, Response]:
    """Use form input to delete a course from the database.

    :param int course_id: The course to delete by ID

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('course_id', course_id, int)

    # Ensure the current user can view the course
    if _get_privilege_level(course_id=course_id) < c.PRIVILEGE_LVL_OWNER:
        abort(403, c.NOT_AUTH_MSG)

    _page_title = 'Delete Course'
    _page_description = 'Delete Course'

    # Verify course exists
    """
    SELECT * FROM COURSES WHERE course_id = 17;
    """
    _course = Course.query.get_or_404(course_id)

    _form = DeleteCourseForm()

    if _form.validate_on_submit():
        try:
            # Delete association data first
            """
            DELETE FROM associations WHERE course_id = 17;
            """
            Association.query.filter(Association.course_id == _course.course_id).delete()
            """
            DELETE FROM courses WHERE course_id = 17;
            """
            db.session.delete(_course)
            db.session.commit()
            flash('Delete successful.')
            return redirect(url_for(c.COURSES_PAGE))
        except Exception as e:
            db.session.rollback()
            flash(f'Deletion failed: {str(e)}', 'error')

    # Default behavior if not sending data to the server (POST, etc.)
    # And re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'delete_course.html',
        page_title=_page_title,
        page_description=_page_description,
        course=_course,
        form=_form,
    )

def _get_privilege_level(course_id: int) -> int:
    """Get the current user's privilege level in the course.

    :param int course_id: The course ID to check against the Association table

    :returns: The privilege level of the user
    :rtype: int
    """
    if current_user.is_admin:
        return 99
    else:
        # Get the ID of the current user
        _member_id = int(current_user.get_id())

        # Ensure the current user has the right privileges
        """
        SELECT roles.role_privilege
        FROM associations,
            roles
        WHERE associations.course_id = 3 AND
            associations.member_id = 2 AND
            associations.role_id = roles.role_id
        LIMIT 1;
        """
        _role_privilege = (db.session.query(Role.role_privilege)
            .join(Association, Association.role_id == Role.role_id)
            .filter(Association.course_id == course_id,
                    Association.member_id == _member_id)
            .first())

        if _role_privilege is None:
            return 0
        else:
            return _role_privilege[0]
