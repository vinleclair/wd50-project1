# imports
from flask import render_template, Blueprint

# config
books_blueprint = Blueprint('books', __name__, template_folder='templates')

# routes
@books_blueprint.route('/')
def index():
    return render_template('index.html')
