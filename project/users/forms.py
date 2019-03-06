from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=40)])
    password = PasswordField('Password', validators=[DataRequired()])
