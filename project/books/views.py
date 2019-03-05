# imports
from flask import render_template, Blueprint
from project.models import Book

# config
books_blueprint = Blueprint('books', __name__, template_folder='templates')

# routes
@books_blueprint.route('/')
def index():
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)
