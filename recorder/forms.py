from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length, Regexp

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
        teacher = Teacher.query.filter_by(staff_number=username.data).first()
        student = Student.query.filter_by(student_number=username.data).first()
        if teacher is not None or student is not None:
            raise ValidationError('existed staff/student number')

    def validate_email(self, email):
        email_prefix = email.data.split("@")[0]
        email_suffix = email.data.split("@")[1]
        if email_suffix != "student.uwa.edu.au" and email_suffix != "uwa.edu.au":
            raise ValidationError('please use uwa mail')
        if email_prefix != self.username.data:
            raise ValidationError('please use your own uwa mail')
        teacher = Teacher.query.filter_by(email=email.data).first()
        student = Student.query.filter_by(email=email.data).first()
        if teacher is not None or student is not None:
            raise ValidationError('existed email address')


# task assign form
class TaskAssignForm(FlaskForm):
    pass
