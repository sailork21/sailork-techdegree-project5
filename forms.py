from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
Length, EqualTo)
from models import Entry


class AddForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()])
    timeSpent = StringField(
        'Time Spent',
        validators=[DataRequired()])
    whatILearned = StringField(
        'What You Learned',
        validators=[DataRequired()])
    ResourcesToRemember = StringField(
        'Resources to Remember',
        validators=[DataRequired()])
