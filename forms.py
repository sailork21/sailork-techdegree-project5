from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
Length, EqualTo)
from wtforms.fields.html5 import DateField
from models import Entry



class AddEditForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()])
    date = DateField(
        'Date',
        )
    duration = StringField(
        'Time Spent',
        validators=[DataRequired()])
    learned = TextAreaField(
        'What You Learned',
        validators=[DataRequired()])
    resources = TextAreaField(
        'Resources to Remember',
        validators=[DataRequired()])
    tag1 = StringField(
        'Tag 1 (optional)',)
    tag2 = StringField(
        'Tag 2 (optional)',)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
