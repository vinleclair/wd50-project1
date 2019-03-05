# imports
from flask import Flask

#config
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

# blueprints
from project.users.views import users_blueprint
from project.books.views import books_blueprint

# register the blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(books_blueprint)
