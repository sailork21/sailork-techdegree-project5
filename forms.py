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
        format='%m/%d/%Y',
        validators=[DataRequired()])
    duration = StringField(
        'Time Spent',
        validators=[DataRequired()])
    learned = TextAreaField(
        'What You Learned',
        validators=[DataRequired()])
    resources = TextAreaField(
        'Resources to Remember',
        validators=[DataRequired()])
