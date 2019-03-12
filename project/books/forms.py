from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField
from wtforms.validators import DataRequired


class AddBookForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])

class BookSearchForm(FlaskForm):
    choices = [('ISBN', 'ISBN'),
               ('Title', 'Title'),
               ('Author', 'Author'),
               ('Year', 'Year')]
    select = SelectField('Search for', choices=choices)
    search = StringField('Value', validators=[DataRequired()])

class ReviewBookForm(FlaskForm):
    rating = RadioField('Rating', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    text = StringField('Text')

