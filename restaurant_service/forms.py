from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import PasswordField, SubmitField, validators
from wtforms.fields.html5 import EmailField


class RegistrationForm(FlaskForm):
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.DataRequired(), validators.Length(min=8, message="Your password must be at least 8 characters")])
    password2 = PasswordField('password2', validators=[validators.DataRequired(), validators.EqualTo('password', message='Passwords must match')])
    submit = SubmitField('submit', [validators.DataRequired()])

class LoginForm(FlaskForm):
    loginemail = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    loginpassword = PasswordField('password', validators=[validators.DataRequired(message='Password field is required')])
    submit = SubmitField('submit', [validators.DataRequired()])
