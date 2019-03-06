# imports
from flask import render_template, Blueprint, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from .forms import RegisterForm
from project import db
from project.models import User


# config
users_blueprint = Blueprint('users', __name__)


# helper functions
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')


# routes
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.username.data, form.password.data)
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering!', 'success')
                return redirect(url_for('books.index'))
            except IntegrityError:
                db.session.rollback()
                flash('ERROR! Username ({}) already exists.'.format(form.username.data), 'error')
    return render_template('register.html', form=form)
