from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User, Post, Event

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user: 
            raise ValidationError('Username taken. Please choose a different one')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user: 
            raise ValidationError('Email taken. Please choose a different one')
            
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user: 
                raise ValidationError('Username taken. Please choose a different one')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user: 
                raise ValidationError('Email taken. Please choose a different one')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Short Description (<250 characters)', validators=[DataRequired()])
    description_long = TextAreaField('Long Description')
    date = DateField('Date', validators=[DataRequired()])
    picture = FileField('Flier', validators=[FileAllowed(['jpeg', 'png'])])
    category = SelectField('Category', choices=[('Art'), ('Music'), ('Theater')])
    tags = StringField('Tags (seperated by commas)')
    submit = SubmitField('Post')