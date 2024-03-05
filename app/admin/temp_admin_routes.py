"""Course administration routing manager.

NOTE - Imports within functions are to prevent a known
circular import problem in Flask.

Test: http://127.0.0.1:5000/add_course
"""
# Flake8 F401: imports are used for type hints
from flask import (Response,  # noqa: F401 pylint:disable=unused-import
                   abort, flash, redirect, render_template, request, url_for)
from flask_login import current_user, login_required
from app import db
from app.admin import admin_bp
from app.admin.admin_forms import (
    AddCourseForm, DeleteCourseForm, EditCourseForm)
from app.models import Course

INDEX_PAGE = 'main.index'


@admin_bp.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    # type: () -> str | Response
    """Use form input to add a course to the database.

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator
    :rtype: str/Response
    """
    # Only administrators can add courses
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    form = AddCourseForm()

    if form.validate_on_submit():
        _course = Course(course_name=form.course_name.data,
                         course_code=form.course_code.data,
                         course_group=form.course_group.data,
                         course_desc=form.course_desc.data)
        db.session.add(_course)
        db.session.commit()
        flash('Course added.')
        return redirect(url_for(INDEX_PAGE))
    else:
        return render_template('admin/add_course.html', title='Add Course',
                               form=form)


@admin_bp.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    # type: (int) -> str | Response
    """Use form input to update a course in the database.

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator
    :rtype: str/Response
    """
    # Only administrators can update courses
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    _course = Course.query.get_or_404(course_id)
    form = EditCourseForm(_course.course_name)

    if form.validate_on_submit():
        _course.course_name = form.course_name.data
        _course.course_code = form.course_code.data
        _course.course_group = form.course_group.data
        _course.course_desc = form.course_desc.dat
        db.session.commit()
        flash('Course updated.')
        return redirect(url_for('main.courses'))
    elif request.method == 'GET':
        form.course_name.data = _course.course_name
        form.course_code.data = _course.course_code
        form.course_group.data = _course.course_group
        form.course_desc.data = _course.course_desc
        return render_template('admin/edit_course.html', title='Edit Course',
                               form=form)
    else:
        abort(500)


@admin_bp.route('/delete_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def delete_course(course_id):
    # type: (int) -> str | Response
    """Use form input to delete a course from the database.

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator
    :rtype: str/Response
    """
    # Only administrators can delete courses
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    _course = Course.query.get_or_404(course_id)
    form = DeleteCourseForm()

    if form.validate_on_submit():
        if form.submit.data:
            db.session.delete(_course)
            db.session.commit()
            flash('Course deleted.')
        return redirect(url_for('main.courses'))
    elif request.method == 'GET':
        _course_name = _course.course_name
        return render_template('admin/delete_course.html',
                               title='Delete Course', course_name=_course_name,
                               form=form)
    else:
        abort(500)
