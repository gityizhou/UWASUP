from flask import render_template, redirect, url_for, flash, request, jsonify, current_app, Response
from flask_uploads import UploadSet, ALL
from flask_login import login_user, current_user, logout_user, login_required

from recorder.email import send_email
from recorder.forms import LoginForm, RegisterForm, SubscribeUnitForm, MakeTeacherForm, PasswdResetForm, \
    PasswdResetRequestForm
from recorder.models.user import User
from recorder.models.unit import Unit
from recorder import db
import random, os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from recorder.models.question import Question
from recorder.models.task import Task
from recorder.models.user_question import User_question
from recorder.models.user_task import User_task

"""
Index page but also our login page!
1. it will check if you are authenticated firstly, if authenticated, redirect to the personal page
2. after click the submit button, it will check account and password
3. teacher: redirect to teacher page
student: redirect to student page
"""


def index():
    # Confirm the login status of the user
    # if authenticated, redirect to his page directly
    if current_user.is_authenticated:
        if current_user.is_teacher == 1:
            return redirect(url_for('teacher_view', staff_number=current_user.user_number))
        if current_user.is_teacher == 0:
            return redirect(url_for('student_view', student_number=current_user.user_number))
    # get the loginForm object
    form = LoginForm()
    if form.validate_on_submit():
        # print(form.username.data)
        user = User.query.filter_by(user_number=form.username.data).first()
        # Verify that the user exists and that the password is correct
        if user is not None and user.check_password(form.password.data):
            # Determine user identity
            if user.is_teacher == 1:  # teacher
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('teacher_view', staff_number=current_user.user_number))
            if user.is_teacher == 0:  # student
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('student_view', student_number=current_user.user_number))
        else:
            # if user not exist or wrong password, give error message
            flash("Invalid username or password, please try again.")
    return render_template('index.html', title="Index", form=form)


# After login, student will be redirected to this page
@login_required
def student_view(student_number):
    student = current_user
    all_units = Unit.query.all()
    form = SubscribeUnitForm()
    form.subscribe_units.choices = [(unit.id, ("{} ({})".format(unit.unit_id, unit.unit_name))) for unit in
                                    Unit.query.all()]
    if form.validate_on_submit():
        for unit_id in form.subscribe_units.data:
            unit_object = Unit.query.get(unit_id)
            student.add_unit(unit_object)
        flash('You have been subscribed to the selected units.')
    student_units = student.units.all()
    return render_template('student_view.html', student=student, student_units=student_units, all_units=all_units,
                           form=form)


# After login, teacher will be redirected to this page
@login_required
def teacher_view(staff_number):
    teacher = current_user
    form_teacher = MakeTeacherForm()
    if form_teacher.validate_on_submit():
        user = User.query.filter_by(user_number=form_teacher.userNumber.data).first()
        user.student2teacher()
        flash('The user now has teacher privileges.')
    teacher_units = teacher.units.all()
    all_units = Unit.query.all()
    all_users = User.query.all()
    return render_template('teacher_view.html', teacher=teacher, teacher_units=teacher_units, all_units=all_units,
                           all_users=all_users, form_teacher=form_teacher)


# logout function
def logout():
    logout_user()
    return redirect(url_for('index'))


def generate_verification_code():
    ''' generate random 6 digit code '''
    code_list = []
    for i in range(10):  # 0-9
        code_list.append(str(i))
    for i in range(65, 91):  # A-Z
        code_list.append(chr(i))
    for i in range(97, 123):  # a-z
        code_list.append(chr(i))

    myslice = random.sample(code_list, 6)
    verification_code = ''.join(myslice)  # list to string
    return verification_code


# register function
def register():
    # get the register form object
    form = RegisterForm()
    # verification_code = generate_verification_code()
    if form.validate_on_submit():
        # read user data from form
        user = User(user_number=form.username.data,
                    first_name=form.firstname.data,
                    last_name=form.lastname.data,
                    email=form.email.data)
        # set the password to hash code
        user.set_password(form.password.data)
        # add the new user to database
        user.add()
        flash('Congratulations. You have registered successfully!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Registration', form=form)


# recorder upload function, the folder now is default /uploads/files/
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


# recorder upload function, the folder now is default /uploads/files/
# and will be uploaded to google drive
def upload():
    files = UploadSet('files', ALL)
    student = current_user
    if request.method == 'POST' and 'upfile' in request.files:
        filename = files.save(
            request.files['upfile'])  # get the file from front end request, return the file name(String)
        url = files.url(filename)  # get the url of this file
        print(student.first_name, student.last_name)
        print(filename)
        print(url)
        upload_file = drive.CreateFile()  # create the google drive file instance
        upload_file.SetContentFile("./uploads/files/" + filename)  # set our file into this instance
        upload_file['title'] = filename  # set the file name of this file
        upload_file.Upload()  # upload this file
        permission = upload_file.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'})
        print(upload_file['alternateLink'])  # Display the sharable link.
        print(upload_file['id'])  # can get this file's google drive-id and use it to save the id into database
        file_id = upload_file['id']
        recorder_url = "https://drive.google.com/uc?authuser=0&id=" + file_id + "&export=download"
        quesion = db.session.query(Question).filter(Question.id == '1').one()    # test only
        User_question.add_user_question(student, quesion, recorder_url)
        os.remove("./uploads/files/" + filename)  # delete this file after uploading it to google drive
    return render_template('recorder.html')



def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswdResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(
                "You should soon receive an email allowing you to reset your \
                password. Please make sure to check your spam and trash \
                if you can't find the email."
            )
            token = user.get_jwt()
            url_password_reset = url_for(
                'password_reset',
                token=token,
                _external=True
            )
            url_password_reset_request = url_for(
                'reset_password_request',
                _external=True
            )
            send_email(
                subject=current_app.config['MAIL_SUBJECT_RESET_PASSWORD'],
                recipients=[user.email],
                text_body=render_template(
                    'email/passwd_reset.txt',
                    url_password_reset=url_password_reset,
                    url_password_reset_request=url_password_reset_request
                ),
                html_body=render_template(
                    'email/passwd_reset.html',
                    url_password_reset=url_password_reset,
                    url_password_reset_request=url_password_reset_request
                )
            )
        return redirect(url_for('index'))
    return render_template('password_reset_request.html', form=form)


def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_jwt(token)
    print(user.first_name)
    if not user:
        return redirect(url_for('index'))
    form = PasswdResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Congratulations. You have already reset your password !", "success")
        return redirect(url_for('index'))
    return render_template(
        'password_reset.html', title='Password Reset', form=form
    )
