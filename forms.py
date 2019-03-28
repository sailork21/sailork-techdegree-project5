from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
Length, EqualTo)
from wtforms.fields.html5 import DateField
from models import User, Entry


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User with that name already exists.")


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=('Username should be one word, letters, '
                'numbers and underscores only.')
            ),
            name_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match!')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()])


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
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
