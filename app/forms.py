from flask import session
from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length

from app import bcrypt
from app.models import User, Book


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username already registered!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already registered!')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('This username does not exist!')


class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    page_count = IntegerField('Page Count', validators=[DataRequired()])
    submit = SubmitField('Add Book')

    def validate_title(self, title):
        book = Book.query.filter_by(title=title.data).first()
        if book:
            raise ValidationError('This book already added!')

    def validate_page_count(self, page_count):
        if page_count.data < 1:
            raise ValidationError('Page count must be greater than zero!')


class UpdateForm(FlaskForm):
    id = IntegerField('Id of book: ', validators=[DataRequired()])
    title = StringField('Title')
    author = StringField('Author')
    page_count = IntegerField('Page Count')
    submit = SubmitField('Update Book')

    def validate_id(self, id):
        book = Book.query.filter_by(id=id.data).first()
        if not book or book.owner_id != session['user_id']:
            raise ValidationError('This book does not exist!')

    def validate_title(self, title):
        books = Book.query.filter_by(owner_id=session.get('user_id')).all()
        for book in books:
            if book.title == title.data:
                raise ValidationError('This book already added!')


class DeleteForm(FlaskForm):
    id = IntegerField('Id of book: ', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Delete Book')

    def validate_id(self, id):
        book = Book.query.filter_by(id=id.data).first()
        if not book or book.owner_id != session['user_id']:
            raise ValidationError('This book does not exist!')

    def validate_password(self, password):
        user = User.query.filter_by(id=session.get('user_id')).first()
        if not bcrypt.check_password_hash(user.password, password.data):
            raise ValidationError('Incorrect password!')
