# imports
from flask import render_template, Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import and_
from sqlalchemy.sql.expression import case
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from datetime import datetime
import requests
import json

from project import db
from project.models import Book, Review, User
from .forms import AddBookForm, BookSearchForm, ReviewBookForm

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

@books_blueprint.route('/search', methods=['GET', 'POST'])
@login_required
def search_book():
    search = BookSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('search_book.html', form=search)

@books_blueprint.route('/results')
@login_required
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'ISBN':
            search_query = db.session.query(Book).filter(Book.isbn.contains(search_string))
        elif search.data['select'] == 'Title':
            search_query = db.session.query(Book).filter(Book.title.contains(search_string))
        elif search.data['select'] == 'Author':
            search_query = db.session.query(Book).filter(Book.author.contains(search_string))
        elif search.data['select'] == 'Year':
            search_query = db.session.query(Book).filter(Book.year == search_string)

    results = search_query.all()
    if not results:
        flash('No results found!', 'error')
        return redirect('/search')
    else:
        print(results)
        return render_template('books.html', books=results)

@books_blueprint.route('/book/<book_id>')
@login_required
def book_details(book_id):
    form = ReviewBookForm(request.form)
    book = db.session.query(Book)\
            .filter(Book.book_id == book_id)\
            .first()
    reviews = db.session.query(Review, User)\
            .outerjoin(User)\
            .filter(Review.book_id == book_id)\
            .filter(Review.user_id == User.user_id)\
            .all()

    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={'key': '53MbEMReRV6qWUw7IDg', "isbns": book.isbn}).json()

    if book is not None:
        return render_template('book_details.html', book=book, reviews=reviews, form=form, goodreads=goodreads)
    else:
        flash('Error! Book does not exist.', 'error')
    return redirect(url_for('books.index'))

@books_blueprint.route('/book/<book_id>', methods=['GET', 'POST'])
@login_required
def review_book(book_id):
    rating = request.form['rating']
    text = request.form['text']
    if request.method == 'POST':
        try:
            new_review = Review(current_user.user_id, book_id, rating, text, datetime.now())
            db.session.add(new_review)
            db.session.commit()
            flash('Review added!', 'success')
        except IntegrityError:
            flash('You already reviewed this book!', 'error')
        return redirect(url_for('books.book_details', book_id=book_id))

@books_blueprint.route("/api/<isbn>", methods=['GET'])
def book_api(isbn):
    if request.method == 'GET':
        book = db.session.query(Book).filter(Book.isbn == isbn).first()
        if book is None:
            return jsonify({"error": "Invalid isbn"}), 404

        reviews = db.session.query(func.count(Review.rating).label('count'), func.avg(Review.rating).label('average'))\
                .filter(Review.book_id == book.book_id)\
                .all()

        return jsonify({
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "isbn": book.isbn,
                "review_count": reviews[0][0],
                "average_score": round(reviews[0][1], 1)
            })
