# imports
from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required
from project import db
from project.models import Book, Review, User
from .forms import AddBookForm
from sqlalchemy import and_
from sqlalchemy.sql.expression import case

# config
books_blueprint = Blueprint('books', __name__)

# helper functions
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')

# routes
@books_blueprint.route('/')
def index():
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)

@books_blueprint.route('/add', methods=['GET', 'POST'])
def add_book():
    form = AddBookForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_book = Book(form.isbn.data, form.title.data, form.author.data, form.year.data)
            db.session.add(new_book)
            db.session.commit()
            flash('New book, {}, added!'.format(new_book.title), 'success')
            return redirect(url_for('books.index'))
        else:
            flash_errors(form)
            flash('ERROR! Book was not added.', 'error')

    return render_template('add_book.html',form=form)

@books_blueprint.route('/book/<book_id>')
@login_required
def book_details(book_id):
    book = db.session.query(Book)\
            .filter(Book.book_id == book_id)\
            .first()
    review = db.session.query(Review, User)\
            .outerjoin(User)\
            .filter(Review.book_id == book_id)\
            .filter(Review.user_id == User.user_id)\
            .all()
    if book is not None:
        return render_template('book_details.html', book=book, review=review)
    else:
        flash('Error! Book does not exist.', 'error')
    return redirect(url_for('books.index'))
