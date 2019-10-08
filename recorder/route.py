from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_uploads import UploadSet, ALL
from flask_login import login_user, current_user, logout_user, login_required
import sys


from recorder.email import send_email
from recorder.forms import LoginForm, RegisterForm, SubscribeUnitForm, MakeTeacherForm, PasswdResetForm, \
    PasswdResetRequestForm, DeleteUserForm, DeleteUnitForm, DeleteTaskForm, DeleteQuestionForm
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
import jwt
import time
import socket

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
        if current_user.is_teacher == 0 and current_user.is_activated == 1:
            return redirect(url_for('student_view', student_number=current_user.user_number))
        else:
            return ('Please verify you email Check your mail box') 
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
    form_make_teacher = MakeTeacherForm()
    form_delete_user = DeleteUserForm()
    form_delete_unit = DeleteUnitForm()
    form_delete_task = DeleteTaskForm()
    form_delete_question = DeleteQuestionForm()
    # make teacher form
    if form_make_teacher.make_teacher_submit.data and form_make_teacher.validate_on_submit():
        staff = User.query.filter_by(user_number=form_make_teacher.staffNumber.data).first()
        staff.student2teacher()
        flash('The user now has teacher privileges.')
    # delete user form
    if form_delete_user.delete_user_submit.data and form_delete_user.validate_on_submit():
        user = User.query.filter_by(user_number=form_delete_user.userNumber.data).first()
        user.delete()
        flash('The user has been deleted.')
    # delete unit form (validation not strictly necessary here for this form, see forms.py)
    if form_delete_unit.delete_unit_submit.data and form_delete_unit.validate_on_submit():
        unit = Unit.query.filter_by(id=form_delete_unit.unitID.data).first()
        unit.delete()
        flash('The unit has been deleted.')
    # delete task form (validation not strictly necessary here for this form, see forms.py)
    if form_delete_task.delete_task_submit.data and form_delete_task.validate_on_submit():
        task = Task.query.filter_by(id=form_delete_task.taskID.data).first()
        task.delete()
        flash('The task has been deleted.')
    # delete question form (validation not strictly necessary here for this form, see forms.py)
    if form_delete_question.delete_question_submit.data and form_delete_question.validate_on_submit():
        question = Question.query.filter_by(id=form_delete_question.questionID.data).first()
        question.delete()
        flash('The question has been deleted.')
    teacher_units = teacher.units.all()
    all_units = Unit.query.all()
    all_users = User.query.all()
    return render_template('teacher_view.html', teacher=teacher, teacher_units=teacher_units, all_units=all_units,
                           all_users=all_users, form_make_teacher=form_make_teacher, form_delete_user=form_delete_user,
                           form_delete_unit=form_delete_unit, form_delete_task=form_delete_task, form_delete_question=form_delete_question)


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
        flash('Congratulations. You have registered successfully! Please verify you email\
            Check your mail box and your Spam!')
        request_email_verification2(form.email.data)
        return redirect(url_for('index'))
    return render_template('register.html', title='Registration', form=form)

def request_email_verification2(email):
    user = User.query.filter_by(email=email).first();
    token = user.get_jwt()
    url = str(url_for("verify_email_by_token",token=token,_external=True))
    body = "link to verify password: "+url
    htmlbody = 'to verify your email click <a href="'+url+'">here</a>'
    send_email(subject="",recipients=[user.email],text_body=body,html_body=htmlbody)
    return "Verification link sent to " + user.email

@login_required
def request_email_verification():
    token = current_user.get_jwt()
    url = str(url_for("verify_email_by_token",token=token,_external=True))
    body = "link to verify password: "+url
    htmlbody = 'to verify your email click <a href="'+url+'">here</a>'
    send_email(subject="",recipients=[current_user.email],text_body=body,html_body=htmlbody)
    return "Verification link sent to " + current_user.email
    
    
@login_required
def verify_email_by_token(token):
    try:
        obj = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
    except:
        return "invalid token"
    email = obj["email"]
    exp = obj["exp"]

    if exp<time.time():
        return "token is expired"
    #enable this check if you want to @login_required this route
    if current_user.email!=email:
          return "invalid token"

    user = User.query.filter_by(email=email).first()
    user.email_is_verified()
    db.session.commit()


    return "Email successfully verified"
    


    
    
    
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
        upload_file['title'] = filename    # set the file name of this file
        upload_file.Upload()        # upload this file
        print(upload_file['id'])    # can get this file's google drive-id and use it to save the id into database
        os.remove("./uploads/files/" + filename)  # delete this file after uploading it to google drive
    return render_template('recorder.html')

def getFilesList():
    upload_file = drive.CreateFile()  # create the google drive file instance
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    res = []
    for file1 in file_list:
        res.append({"title":file1['title'],"id":file1['id']})
    return jsonify(res)
    #return res;


def donwload(id,title):
    file = drive.CreateFile({'id': id})
    file.GetContentFile('./downloads/'+title) # Download file as 'studentnumber.mp3'.
    return redirect(url_for('send_download',filename=title));
    

def download_access(filename):
    return send_file('../downloads/'+filename,as_attachment=True)

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
