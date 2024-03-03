"""Administration routing manager.

NOTE - Imports within functions are to prevent a known
circular import problem in Flask.

Test: http://127.0.0.1:5000/create_user
"""
# Flake8 F401: imports are used for type hints
from flask import (Response,  # noqa: F401
                   flash, redirect, render_template, url_for)
from flask_login import current_user, login_user, logout_user
from app.admin import admin_bp
from app.admin.admin_forms import CreateUserForm
from app import db
from app.models import User

# ...

@admin_bp.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if  current_user.get_id() != 1:
        return redirect(url_for('main.index'))
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, user_email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User added.')
        return redirect(url_for('main.users'))
    return render_template('admin/create_user.html', title='Create User', form=form)
