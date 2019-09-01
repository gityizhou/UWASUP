from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from recorder.models.teacher import Teacher
from recorder.models.student import Student


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Sign In')


# user register form
class RegisterForm(FlaskForm):
    pass


# task assign form
class TaskAssignForm(FlaskForm):
    pass
