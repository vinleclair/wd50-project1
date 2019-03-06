from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AddBookForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
