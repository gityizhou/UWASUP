from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField, DateField, TimeField, DateTimeField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length, Regexp, Required
from wtforms.widgets import ListWidget, CheckboxInput

from recorder.models.user import User
from recorder.models.unit import Unit
from recorder.models.task import Task
from recorder.models.question import Question

import sys


############################
# forms needed for registration, login and password reset
############################


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
                                                                               message="UWA student/staff numbers should be 8 digits.")])

    firstname = StringField("First Name (as per LMS)", validators=[DataRequired()])
    lastname = StringField("Last Name (as per LMS)", validators=[DataRequired()])
    email = StringField("UWA Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=18,
                                                                            message="Please use more than 7 characters.")])
    password2 = PasswordField(
        "Password Repeat", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # check if your username is already existed in database
        user = User.query.filter_by(user_number=username.data).first()
        if user is not None:
            raise ValidationError('This student/staff number is already in use.')

    def validate_email(self, email):
        # this function will basicly split the address into 2 parts
        # check if your mail is UWA mail
        # check if your mail is already existed in database
        if "@" not in email.data:
            raise ValidationError('Please use a valid email address.')
        email_prefix = email.data.split("@")[0]
        email_suffix = email.data.split("@")[1]

        if email_suffix != "student.uwa.edu.au" and email_suffix != "uwa.edu.au":
            raise ValidationError('You must use a UWA email account.')
        if email_prefix != self.username.data:
            raise ValidationError('Please use your own student email.')
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already in use.')

class PasswdResetRequestForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(
                'You do not have an account for this email address')

class PasswdResetForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=18,
                                                                            message="Length of password should longer than 7")])
    password2 = PasswordField(
        "Password Repeat", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')


############################
# forms needed in student_view.html
############################


# field needed for SubscribeUnitForm (below) in student_view.html
class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class SubscribeUnitForm(FlaskForm):
    subscribe_units = MultiCheckboxField('Units', [DataRequired(message='Please select one or more units.')],
                                         coerce=int)
    submit = SubmitField('Subscribe')


############################
# forms needed in teacher_view.html
############################

class MakeTeacherForm(FlaskForm):
    staffNumber = StringField('Staff Number', validators=[DataRequired()])
    make_teacher_submit = SubmitField('Make User a Teacher')

    def validate_staffNumber(self, staffNumber):
        staff = User.query.filter_by(user_number=staffNumber.data).first()
        if staff is None:
            raise ValidationError('This user does not exist.')

class DeleteUserForm(FlaskForm):
    userNumber = StringField('User Number', validators=[DataRequired()])
    delete_user_submit = SubmitField('Delete User')

    def validate_userNumber(self, userNumber):
        user = User.query.filter_by(user_number=userNumber.data).first()
        if user is None:
            raise ValidationError('This user does not exist.')

class CreateUnitForm(FlaskForm):
    unitID = StringField('Unit code', validators=[DataRequired()])
    unitName = StringField('Unit name', validators=[DataRequired()])
    create_unit_submit = SubmitField('Create Unit')

    def validate_unitID(self, unitID):
        # checks for only alphanumeric characters
        if not unitID.data.isalnum():
            raise ValidationError('Unit code must contain only uppercase letters and numbers.')
        # ensures letters are uppercase and code contains both letters and numbers
        else:
            hasLetters = False
            hasNumbers = False
            for char in unitID.data:
                if not char.isdigit():
                    hasLetters = True
                    if not char.isalpha():
                        raise ValidationError('Unit code must contain only uppercase letters and numbers.')
                else:
                    hasNumbers = True
        if not hasNumbers:
            raise ValidationError('Unit code must contain numbers.')
        elif not hasLetters:
            raise ValidationError('Unit code must contain uppercase letters.')
        else:
            unit = Unit.query.filter_by(unit_id=unitID.data).first()
            if unit is not None:
                raise ValidationError('This unit already exists.')

class EditUnitForm(FlaskForm):
    current_unitID = StringField('Current Unit code')
    edit_unitID = StringField('Edit Unit code')
    edit_unitName = StringField('Edit Unit name')
    edit_unit_submit = SubmitField('Update Unit')

    def validate_edit_unitID(self, edit_unitID):
        # checks for only alphanumeric characters
        if not edit_unitID.data.isalnum():
            raise ValidationError('Unit code must contain only uppercase letters and numbers.')
        # ensures letters are uppercase and code contains both letters and numbers
        else:
            hasLetters = False
            hasNumbers = False
            for char in edit_unitID.data:
                if not char.isdigit():
                    hasLetters = True
                    if not char.isalpha():
                        raise ValidationError('Unit code must contain only uppercase letters and numbers.')
                else:
                    hasNumbers = True
        if not hasNumbers:
            raise ValidationError('Unit code must contain numbers.')
        elif not hasLetters:
            raise ValidationError('Unit code must contain uppercase letters.')

class AddTaskForm(FlaskForm):
    taskName = StringField('Task name', validators=[DataRequired()])
    taskDescription = StringField('Description', validators=[DataRequired()])
    taskDueDate = DateTimeField('Due date (YYYY-MM-DD)')
    taskDueTime = TimeField('Due time in 24h format (HH:MM)')
    task_unitID = StringField('Description')
    pdfTitle = StringField('PDF Attachment Title')
    add_task_submit = SubmitField('Add Task')

# validators not needed as this form will only be generated for existing units
class DeleteUnitForm(FlaskForm):
    del_unitID = StringField()
    delete_unit_submit = SubmitField('Delete Unit')

# validators not needed as this form will only be generated for existing tasks
class DeleteTaskForm(FlaskForm):
    del_taskID = StringField()
    delete_task_submit = SubmitField('Delete Task')

# validators not needed as this form will only be generated for existing questions
class DeleteQuestionForm(FlaskForm):
    del_questionID = StringField()
    delete_question_submit = SubmitField('Delete Question')


