from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length, Regexp, Required
from wtforms.widgets import ListWidget, CheckboxInput

from recorder.models.user import User

import sys


# user login form
class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    # data required validation for username and password
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField('Sign In')


# user register form
class RegisterForm(FlaskForm):
    """ registration form validation rules
    1. all data required
    2. username must be 8-digit number
    3. email must be valid and should be UWA mail
        student.uwa.edu.au   or   uwa.edu.au, can add more because I dont know others
    4. password should be longer than 8-digit and should be a mixture of alphabets and number
    5. repeat password should be the same as password
    6. username, email should not be existed in current database.
    """

    username = StringField("Student Number / Staff Number", validators=[DataRequired(),
                                                                        Length(min=8, max=8,
                                                                               message="UWA student/staff number should be 8 digits number.")])

    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    reg = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
    password = PasswordField("Password", validators=[DataRequired(), Regexp(reg,
                                                                            message="Length of password should longer than 8 with numbers and alphabets.")])
    password2 = PasswordField(
        "Password Repeat", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # check if your username is already existed in database
        user = User.query.filter_by(user_number=username.data).first()
        if user is not None:
            raise ValidationError('existed staff/student number')

    def validate_email(self, email):
        # this function will basicly split the address into 2 parts
        # check if your mail is UWA mail
        # check if your mail is already existed in database
        if "@" not in email.data:
            raise ValidationError('please input a valid email address')
        email_prefix = email.data.split("@")[0]
        email_suffix = email.data.split("@")[1]

        if email_suffix != "student.uwa.edu.au" and email_suffix != "uwa.edu.au":
            raise ValidationError('please use uwa mail')
        if email_prefix != self.username.data:
            raise ValidationError('please use your own uwa mail')
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('existed email address')

# form for students to subscribe themselves to units (student_view.html)
class MultiCheckboxField(SelectMultipleField):
    widget			= ListWidget(prefix_label=False)
    option_widget	= CheckboxInput()
class SubscribeUnitForm(FlaskForm):
    subscribe_units = MultiCheckboxField('Units', [Required(message='Please select one or more units.')], coerce=int)
    submit = SubmitField('Subscribe')

