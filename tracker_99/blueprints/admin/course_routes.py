"""Course Administration Routing Manager.
"""

from typing import Union

from flask import Response, flash, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from tracker_99 import db
from tracker_99.app_utils import validate_input
from tracker_99.blueprints.admin import admin_bp
from tracker_99.blueprints.admin.admin_forms import (
    AddCourseForm,
    EditCourseForm,
    DeleteCourseForm,
)
from tracker_99.models.models import Course, Association

INDEX_PAGE = 'main_bp.index'
COURSES_PAGE = 'main_bp.courses'
NOT_AUTH_MSG = 'You do not have permission to perform that action.'


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
            """
            INSERT INTO courses (course_name, course_code, course_group, course_desc)
            VALUES ("Building Bad Python Applications", "SDEV 301", "SDEV", "Not recommended!");
            """
            db.session.add(_course)
            db.session.commit()

            # Get row_id of the new course
            _new_id = _course.course_id

            # Add the course and chair to the association table
            _member_id = int(current_user.get_id())
            _assoc = Association(course_id=_new_id, role_id=1, member_id=_member_id)

            db.session.add(_assoc)
            db.session.commit()

            flash('Addition successful.')
            return redirect(url_for(COURSES_PAGE))
        except SQLAlchemyError as e:
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

    _page_title = 'View Course'
    _page_description = 'View Course'

    # Verify course exists
    """
    SELECT * FROM courses WHERE course_id = 17;
    """
    _course = Course.query.get_or_404(course_id)

    return render_template(
        'view_course.html',
        page_title=_page_title,
        page_description=_page_description,
        course=_course,
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

    _page_title = 'Edit Course'
    _page_description = 'Edit Course'

    # Verify course exists
    """
    SELECT * FROM courses WHERE course_id = 17;
    """
    _course = Course.query.get_or_404(course_id)
    _form = EditCourseForm()

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
            _course.course_desc = _form.course_desc.data
            """
            UPDATE courses
            SET course_name = "Building Better Python Applications",
                course_code = "SDEV 305",
                course_group = "SDEV",
                course_desc = "Better than before!"
            WHERE course_id = 17;
            """
            # db.session.add(_course)
            db.session.commit()
            flash('Update successful.')
            return redirect(url_for(COURSES_PAGE))
        except SQLAlchemyError as e:
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
            return redirect(url_for(COURSES_PAGE))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Delete failed: {str(e)}', 'error')

    # Default behavior if not sending data to the server (POST, etc.)
    # And re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'delete_course.html',
        page_title=_page_title,
        page_description=_page_description,
        course=_course,
        form=_form,
    )
