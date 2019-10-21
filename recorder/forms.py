from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField, DateField, TimeField, \
    DateTimeField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length, Regexp, Required
from wtforms.widgets import ListWidget, CheckboxInput

from recorder.models.user import User
from recorder.models.unit import Unit
from recorder.models.task import Task
from recorder.models.user_unit import User_unit
from recorder.models.question import Question

import sys, datetime, time


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

    username = StringField("Student/Staff Number", validators=[DataRequired(),
                                                                        Length(min=8, max=8,
                                                                               message="UWA student/staff numbers should be 8 digits.")])

    firstname = StringField("First Name (as per LMS)", validators=[DataRequired()])
    lastname = StringField("Last Name (as per LMS)", validators=[DataRequired()])
    email = StringField("UWA Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=18,
                                                                            message="Minimum length of 8 characters and no special characters.")])
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
    email = StringField("Email Address:", validators=[DataRequired(), Email()])
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
    studentID = StringField('Student number')
    subscribe_unit_submit = SubmitField('Subscribe')

    def validate_subscribe_units(self, subscribe_units):
        for u in subscribe_units.data:
            user_unit = User_unit.query.filter_by(user_id=self.studentID.data,
                                              unit_id=u).first()
            if user_unit is not None:
                raise ValidationError('You are already subscribed to one or more of these units.')

# validators not needed as this form will only be generated for existing units
class UnsubscribeUnitForm(FlaskForm):
    unsub_unitID = StringField()
    unsub_studentID = StringField()
    unsubscribe_unit_submit = SubmitField('Unsubscribe from Unit')


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
            raise ValidationError('Character error Unit code must contain only uppercase letters and numbers.')
        # ensures letters are uppercase and code contains both letters and numbers
        else:
            hasLetters = False
            hasNumbers = False
            letterCount = 0
            numberCount = 0
            for char in unitID.data:
                if not char.isdigit():
                    hasLetters = True
                    letterCount += 1
                    if not char.isupper():
                        raise ValidationError('Unit code must not contain lowercase letters.')
                else:
                    numberCount += 1
                    hasNumbers = True
        if not hasNumbers:
            raise ValidationError('Unit code must contain numbers.')
        elif not hasLetters:
            raise ValidationError('Unit code must contain uppercase letters.')
        elif numberCount != 4 or letterCount != 4:
            raise ValidationError('Unit code must be four letters and four numbers.')
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
            raise ValidationError('Character error Unit code must contain only uppercase letters and numbers.')
        # ensures letters are uppercase and code contains both letters and numbers
        else:
            hasLetters = False
            hasNumbers = False
            letterCount = 0
            numberCount = 0
            for char in edit_unitID.data:
                if not char.isdigit():
                    hasLetters = True
                    letterCount += 1
                    if not char.isupper():
                        raise ValidationError('Unit code must not contain lowercase letters.')
                else:
                    numberCount += 1
                    hasNumbers = True
        if not hasNumbers:
            raise ValidationError('Unit code must contain numbers.')
        elif not hasLetters:
            raise ValidationError('Unit code must contain uppercase letters.')
        elif numberCount != 4 or letterCount != 4:
            raise ValidationError('Unit code must be four letters and four numbers.')
        else:
            unit = Unit.query.filter_by(unit_id=edit_unitID.data).first()
            if unit is None:
                raise ValidationError('This unit does not exist.')

class AddTaskForm(FlaskForm):
    taskName = StringField('Task name', validators=[DataRequired()])
    taskDescription = StringField('Description', validators=[DataRequired()])
    taskDueDate = StringField('Due date (YYYY-MM-DD)')
    taskDueTime = StringField('Due time in 24h format (HH:MM)')
    task_unitID = StringField('unitID')
    pdfTitle = StringField('PDF Attachment Title')
    add_task_submit = SubmitField('Publish Task')

    def validate_taskDueDate(self, taskDueDate):
        if taskDueDate.data:
            if self.taskDueTime.data:
                try:
                    datetime.datetime.strptime(taskDueDate.data, '%Y-%m-%d')
                except ValueError:
                    raise ValidationError('Due date must be in format YYYY-MM-DD.')
            else:
                raise ValidationError('Due date must also have a due time.')

    def validate_taskDueTime(self, taskDueTime):
        if taskDueTime.data:
            if self.taskDueDate.data:
                try:
                    time.strptime(taskDueTime.data, '%H:%M')
                except ValueError:
                    raise ValidationError('Due time must be in format HH:MM.')
            else:
                raise ValidationError('Due time must also have a due date.')

class EditTaskForm(FlaskForm):
    current_taskID = StringField('Current taskID')
    edit_taskName = StringField('Task name', validators=[DataRequired()])
    edit_taskDescription = StringField('Description', validators=[DataRequired()])
    edit_taskDueDate = StringField('Due date (YYYY-MM-DD)')
    edit_taskDueTime = StringField('Due time in 24h format (HH:MM)')
    edit_task_submit = SubmitField('Update Task')

    def validate_edit_taskDueDate(self, edit_taskDueDate):
        if edit_taskDueDate.data:
            if self.edit_taskDueTime.data:
                try:
                    datetime.datetime.strptime(edit_taskDueDate.data, '%Y-%m-%d')
                except ValueError:
                    raise ValidationError('Due date must be in format YYYY-MM-DD.')
            else:
                raise ValidationError('Due date must also have a due time.')

    def validate_edit_taskDueTime(self, edit_taskDueTime):
        if edit_taskDueTime.data:
            if self.edit_taskDueDate.data:
                try:
                    time.strptime(edit_taskDueTime.data, '%H:%M')
                except ValueError:
                    raise ValidationError('Due time must be in format HH:MM.')
            else:
                raise ValidationError('Due time must also have a due date.')

class AddQuestionForm(FlaskForm):
    questionName = StringField('Question name', validators=[DataRequired()])
    questionDescription = StringField('Description', validators=[DataRequired()])
    question_taskID = StringField('taskID')
    add_question_submit = SubmitField('Publish Question')

class TaskFeedbackForm(FlaskForm):
    feedbackStudentID = StringField('studentID')
    feedbackTaskID = StringField('taskID')
    mark = StringField('Mark (format 00.0)')
    #feedbackRecorderUrl = StringField('feedbackURL')
    feedbackComment = TextAreaField('Comments')
    task_feedback_submit = SubmitField('Update Mark and Comments')

    def validate_mark(self, mark):
        hasLetters = False
        for char in mark.data:
            if not char.isdigit() and char != '.':
                hasLetters = True
        if hasLetters:
            raise ValidationError("Mark must not include letters or characters other than '.'")
        if len(mark.data) != 4:
            raise ValidationError('Mark must be four characters.')
        if mark.data[2] != '.':
            raise ValidationError('Mark must be in the format 00.0')


class EditQuestionForm(FlaskForm):
    edit_questionName = StringField('Question name', validators=[DataRequired()])
    edit_questionDescription = StringField('Description', validators=[DataRequired()])
    current_questionID = StringField('questionID')
    edit_question_submit = SubmitField('Update Question')

# validators not needed as this form will only be generated for existing units
class DeleteUnitForm(FlaskForm):
    del_unitID = StringField()
    delete_unit_submit = SubmitField('Delete Unit')

# validators not needed as this form will only be generated for existing tasks
class DeleteTaskForm(FlaskForm):
    del_taskID = StringField()
    delete_task_submit = SubmitField('Delete Task')

# validators not needed as this form will only be generated for existing tasks
class DeletePDFForm(FlaskForm):
    del_pdf_taskID = StringField()
    delete_pdf_submit = SubmitField('Delete PDF')

# validators not needed as this form will only be generated for existing questions
class DeleteQuestionForm(FlaskForm):
    del_questionID = StringField()
    delete_question_submit = SubmitField('Delete Question')


