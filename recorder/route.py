from flask import render_template, redirect, url_for, flash, request, jsonify, current_app, send_from_directory
from flask_uploads import UploadSet, ALL
from flask_login import login_user, current_user, logout_user, login_required

from recorder.email import send_email
from recorder.forms import LoginForm, RegisterForm, SubscribeUnitForm, MakeTeacherForm, PasswdResetForm, \
    PasswdResetRequestForm, DeleteUserForm, DeleteUnitForm, DeleteTaskForm, DeleteQuestionForm, CreateUnitForm, \
    EditUnitForm, AddTaskForm, EditTaskForm, AddQuestionForm, EditQuestionForm, UnsubscribeUnitForm, DeletePDFForm, \
    TaskFeedbackForm
from recorder.models.user import User
from recorder.models.unit import Unit
from recorder.models.user_unit import User_unit
from recorder import db
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from recorder.models.question import Question
from recorder.models.task import Task
from recorder.models.user_question import User_question
from recorder.models.user_task import User_task
import os, jwt, time, datetime, sys
from pandas import DataFrame
from recorder import autodelete

# # google verification
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
DOMAIN_NAME = "http://localhost:5000"

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
        if current_user.is_teacher == 1 and current_user.is_activated == 1:
            return redirect(url_for('teacher_view', staff_number=current_user.user_number))
        if current_user.is_teacher == 0 and current_user.is_activated == 1:
            return redirect(url_for('student_view', student_number=current_user.user_number))
        else:
            return "error"
            #return redirect(url_for('not_activated'))
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

def not_activated():
    print("")
    return render_template('not_activated.html')

# After login, student will be redirected to this page
@login_required
def student_view(student_number):
    student = current_user
    answered_questions_IDs = []
    answered_questions = User_question.query.filter_by(user_id=student.id)
    for record in answered_questions:
        answered_questions_IDs.append(record.question_id)
    form_subscribe_unit = SubscribeUnitForm()
    form_unsubscribe_unit = UnsubscribeUnitForm()
    form_subscribe_unit.subscribe_units.choices = [(unit.id, ("{} ({})".format(unit.unit_id, unit.unit_name))) for unit
                                                   in
                                                   Unit.query.all()]
    if form_subscribe_unit.validate_on_submit():
        for unit_id in form_subscribe_unit.subscribe_units.data:
            unit_object = Unit.query.get(unit_id)
            student.add_unit(unit_object)
        flash('You have been subscribed to the selected units.')
    student_units = student.get_student_units()
    # unsubscribe from unit form (validation not strictly necessary here for this form, see forms.py)
    if form_unsubscribe_unit.unsubscribe_unit_submit.data and form_unsubscribe_unit.validate_on_submit():
        user_unit = User_unit.query.filter_by(user_id=form_unsubscribe_unit.unsub_studentID.data,
                                              unit_id=form_unsubscribe_unit.unsub_unitID.data).first()
        user_unit.delete()
        # add in any function for deleting user_task and user_question entries assco with this user_unit
        flash('You have been unsubscribed from the unit.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('student_view', student_number=student_number))
    return render_template('student_view.html', student=student, student_units=student_units,
                           form_subscribe_unit=form_subscribe_unit, form_unsubscribe_unit=form_unsubscribe_unit,
                           answered_questions_IDs=answered_questions_IDs)


# After login, teacher will be redirected to this page
@login_required
def teacher_view(staff_number):
    teacher = current_user
    form_make_teacher = MakeTeacherForm()
    form_delete_user = DeleteUserForm()
    form_create_unit = CreateUnitForm()
    form_edit_unit = EditUnitForm()
    form_delete_unit = DeleteUnitForm()
    form_add_task = AddTaskForm()
    form_edit_task = EditTaskForm()
    form_delete_task = DeleteTaskForm()
    form_delete_pdf = DeletePDFForm()
    form_add_question = AddQuestionForm()
    form_edit_question = EditQuestionForm()
    form_delete_question = DeleteQuestionForm()
    form_task_feedback = TaskFeedbackForm()

    incoming_current_student_button_id = None
    # make teacher form
    if form_make_teacher.make_teacher_submit.data and form_make_teacher.validate_on_submit():
        staff = User.query.filter_by(user_number=form_make_teacher.staffNumber.data).first()
        staff.student2teacher()
        flash('The user now has teacher privileges.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('teacher_view', staff_number=staff_number))
    # delete user form
    if form_delete_user.delete_user_submit.data and form_delete_user.validate_on_submit():
        user = User.query.filter_by(user_number=form_delete_user.userNumber.data).first()
        user.delete()
        flash('The user has been deleted.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('teacher_view', staff_number=staff_number))
    # create unit form
    if form_create_unit.create_unit_submit.data and form_create_unit.validate_on_submit():
        unit = Unit(unit_id=form_create_unit.unitID.data, unit_name=form_create_unit.unitName.data)
        unit.add()
        user = User.query.filter_by(user_number=staff_number).first()
        unit = Unit.query.filter_by(unit_name=form_create_unit.unitName.data).first()
        user.add_unit(unit)
        flash('The unit has been created.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('teacher_view', staff_number=staff_number))
    # edit unit form
    if form_edit_unit.edit_unit_submit.data and form_edit_unit.validate_on_submit():
        unit = Unit.query.filter_by(unit_id=form_edit_unit.current_unitID.data).first()
        unit.unit_id = form_edit_unit.edit_unitID.data
        unit.unit_name = form_edit_unit.edit_unitName.data
        unit.update()
        flash('The unit has been updated.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('teacher_view', staff_number=staff_number))
    # delete unit form (validation not strictly necessary here for this form, see forms.py)
    if form_delete_unit.delete_unit_submit.data and form_delete_unit.validate_on_submit():
        unit = Unit.query.filter_by(id=form_delete_unit.del_unitID.data).first()
        unit.delete()
        flash('The unit has been deleted.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('teacher_view', staff_number=staff_number))
    # add task form
    if form_add_task.add_task_submit.data and form_add_task.validate_on_submit():
        # create DateTime format "YYYY-MM-DD HH:MM"
        if form_add_task.taskDueDate.data and form_add_task.taskDueTime.data:
            due_date = form_add_task.taskDueDate.data
            due_time = form_add_task.taskDueTime.data
            due_date_time = due_date + " " + due_time
            datetime_obj = datetime.datetime.strptime(due_date_time, '%Y-%m-%d %H:%M')
        else:
            datetime_obj = None
        task = Task(
            task_name=form_add_task.taskName.data,
            description=form_add_task.taskDescription.data,
            due_time=datetime_obj,
            unit_id=form_add_task.task_unitID.data)
        task.add()
        task = Task.query.filter_by(id=task.id).first()
        unit = Unit.query.filter_by(id=form_add_task.task_unitID.data).first()
        task.add_task2unit(unit)
        # deletes MP3s older than one month in Google Drive when new tasks are created
        autodelete.delete_old_recordings()
        flash('The task has been added.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('teacher_view', staff_number=staff_number))
    # edit task form
    if form_edit_task.edit_task_submit.data and form_edit_task.validate_on_submit():
        # create DateTime format "YYYY-MM-DD HH:MM"
        if form_edit_task.edit_taskDueDate.data and form_edit_task.edit_taskDueTime.data:
            due_date = form_edit_task.edit_taskDueDate.data
            due_time = form_edit_task.edit_taskDueTime.data
            due_date_time = due_date + " " + due_time
            datetime_obj = datetime.datetime.strptime(due_date_time, '%Y-%m-%d %H:%M')
        else:
            datetime_obj = None
        task = Task.query.filter_by(id=form_edit_task.current_taskID.data).first()
        task.task_name = form_edit_task.edit_taskName.data
        task.description = form_edit_task.edit_taskDescription.data
        task.due_time = datetime_obj
        task.update()
        flash('The task has been updated.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('teacher_view', staff_number=staff_number))
    # delete task form (validation not strictly necessary here for this form, see forms.py)
    if form_delete_task.delete_task_submit.data and form_delete_task.validate_on_submit():
        task = Task.query.filter_by(id=form_delete_task.del_taskID.data).first()
        task.delete()
        flash('The task has been deleted.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('teacher_view', staff_number=staff_number))
    # delete pdf form (validation not strictly necessary here for this form, see forms.py)
    if form_delete_pdf.delete_pdf_submit.data and form_delete_pdf.validate_on_submit():
        task = Task.query.filter_by(id=form_delete_pdf.del_pdf_taskID.data).first()
        task.delete_pdf()
        flash('The file has been deleted.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('teacher_view', staff_number=staff_number))
    # task feedback form
    if form_task_feedback.task_feedback_submit.data and form_task_feedback.validate_on_submit():
        if form_task_feedback.mark.data == "":
            mark = None
        else:
            mark = float(form_task_feedback.mark.data)
        user_task = User_task.query.filter_by(task_id=form_task_feedback.feedbackTaskID.data,
                                              user_id=form_task_feedback.feedbackStudentID.data).first()
        user_task.comment = form_task_feedback.feedbackComment.data
        user_task.mark = mark
        user_task.update()
        current_student_button_id =  "#btn-open-student-accordian-" + form_task_feedback.feedbackStudentID.data + "-" + form_task_feedback.feedbackTaskID.data
        current_student_submissions_button_id = "#btn-open-submission-accordian-" + form_task_feedback.feedbackUnitID.data + "-" + form_task_feedback.feedbackTaskID.data
        current_task_button_id = "#btn-open-task-accordian-" + form_task_feedback.feedbackUnitID.data + "-" + form_task_feedback.feedbackTaskID.data
        current_unit_button_id = "#btn-open-unit-accordian-" + form_task_feedback.feedbackUnitID.data
        # need to return redirect on successful submission to clear form fields
        all_units = Unit.query.all()
        all_users = User.query.all()
        return render_template('teacher_view.html', teacher=teacher, all_units=all_units, all_users=all_users,
                            form_make_teacher=form_make_teacher, form_delete_user=form_delete_user,
                            form_delete_unit=form_delete_unit, form_delete_task=form_delete_task,
                            form_delete_question=form_delete_question, form_create_unit=form_create_unit,
                            form_edit_unit=form_edit_unit, form_add_task=form_add_task,
                            form_edit_task=form_edit_task, form_add_question=form_add_question,
                            form_edit_question=form_edit_question, DOMAIN_NAME=DOMAIN_NAME,
                            form_delete_pdf=form_delete_pdf, form_task_feedback=form_task_feedback,
                            current_student_button_id=current_student_button_id,
                            current_student_submissions_button_id=current_student_submissions_button_id,
                            current_task_button_id=current_task_button_id,
                            current_unit_button_id=current_unit_button_id)
    # add question form
    if form_add_question.add_question_submit.data and form_add_question.validate_on_submit():
        question = Question(
            question_name=form_add_question.questionName.data,
            description=form_add_question.questionDescription.data,
            task_id=form_add_question.question_taskID.data)
        question.add()
        question = Question.query.filter_by(id=question.id).first()
        task = Task.query.filter_by(id=form_add_question.question_taskID.data).first()
        question.add_question2task(task)
        flash('The question has been addedd.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('teacher_view', staff_number=staff_number))
    # edit question form
    if form_edit_question.edit_question_submit.data and form_edit_question.validate_on_submit():
        question = Question.query.filter_by(id=form_edit_question.current_questionID.data).first()
        question.question_name = form_edit_question.edit_questionName.data
        question.description = form_edit_question.edit_questionDescription.data
        question.update()
        flash('The question has been updated.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('teacher_view', staff_number=staff_number))
    # delete question form (validation not strictly necessary here for this form, see forms.py)
    if form_delete_question.delete_question_submit.data and form_delete_question.validate_on_submit():
        question = Question.query.filter_by(id=form_delete_question.del_questionID.data).first()
        question.delete()
        flash('The question has been deleted.')
        # need to return redirect on successful submission to clear form fields
        return redirect(url_for('teacher_view', staff_number=staff_number))
    all_units = Unit.query.all()
    all_users = User.query.all()
    return render_template('teacher_view.html', teacher=teacher, all_units=all_units, all_users=all_users,
                form_make_teacher=form_make_teacher, form_delete_user=form_delete_user,
                form_delete_unit=form_delete_unit, form_delete_task=form_delete_task,
                form_delete_question=form_delete_question, form_create_unit=form_create_unit,
                form_edit_unit=form_edit_unit, form_add_task=form_add_task,
                form_edit_task=form_edit_task, form_add_question=form_add_question,
                form_edit_question=form_edit_question, DOMAIN_NAME=DOMAIN_NAME,
                form_delete_pdf=form_delete_pdf, form_task_feedback=form_task_feedback)


# logout function
def logout():
    logout_user()
    return redirect(url_for('index'))


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
        flash(
            'Congratulations. You have registered successfully! Please verify you email before logging in. Check your email inbox and spam folder.')
        request_email_verification2(form.email.data)
        return redirect(url_for('index'))
    return render_template('register.html', title='Registration', form=form)


def request_email_verification2(email):
    user = User.query.filter_by(email=email).first()
    token = user.get_jwt()
    url = str(url_for("verify_email_by_token", token=token, _external=True))
    body = "link to verify password: " + url
    htmlbody = 'Thanks for registering for SUP! To verify your email click <a href="' + url + '">here</a>'
    send_email(subject="", recipients=[user.email], text_body=body, html_body=htmlbody)
    return "Verification link sent to " + user.email + "Please check you Spam box as well"


@login_required
def request_email_verification():
    token = current_user.get_jwt()
    url = str(url_for("verify_email_by_token", token=token, _external=True))
    body = "Link to verify password: " + url  # this is also can be a separate template but this msg can be enough
    htmlbody = 'Thanks for registering for SUP! To verify your email click <a href="' + url + '">here</a>'
    send_email(subject="", recipients=[current_user.email], text_body=body, html_body=htmlbody)
    return "Verification link sent to " + current_user.email


@login_required
def verify_email_by_token(token):
    try:
        obj = jwt.decode(token, current_app.config['SECRET_KEY'],
                         algorithms=['HS256'])  # will decode the token which has been send to email
    except:
        return "invalid token"
    email = obj["email"]
    exp = obj["exp"]

    if exp < time.time():
        return "token is expired"
    # enable this check if you want to @login_required this route
    if current_user.email != email:
        return "invalid token"

    user = User.query.filter_by(email=email).first()
    user.email_is_verified()
    db.session.commit()  # this will change user is verified in data base from 0 to 1

    # it will return to login page after verify the account 
    # return "Email successfully verified"
    # return render_template('index.html', title="Index", form=form)
    return render_template('index.html', title="Index")


# record upload function, the folder now is default /uploads/files/
# and will be uploaded to google drive
def upload():
    files = UploadSet('files', ALL)
    student_number = current_user.user_number
    user_id = current_user.id
    question_id = request.form.get("question_id")
    user_question = User_question.query.filter_by(question_id=question_id,
                                                  user_id=user_id).first()

    print(user_question)
    if question_id:
        question_id = int(request.form.get("question_id"))  # get the question id from request post
        question_id_str = str(question_id)
        this_question = db.session.query(Question).filter(Question.id == question_id).one()
        task_id = this_question.task_id
        this_task = db.session.query(Task).filter(Task.id == task_id).one()

        user_task = User_task.query.filter_by(task_id=task_id, user_id=user_id).first()
        task_id_str = str(task_id)
        unit_id = db.session.query(Task).filter(Task.id == task_id).one().unit_id
        unit_id_str = str(unit_id)
        print(student_number)
        print(unit_id_str)
        print(task_id_str)
        print(question_id_str)
        name = student_number + '_' + unit_id_str + '_' + task_id_str + '_' + question_id_str + '.mp3'

    if not user_task:
        User_task.add_user_task(user=current_user, task=this_task)  # save user_question to db

    if request.method == 'POST' and 'upfile' in request.files:
        filename = files.save(
            request.files['upfile'])  # get the file from front end request, return the file name(String)
        if user_question:
            record_id = user_question.record_id
            upload_file = drive.CreateFile({'id': record_id})
            upload_file.SetContentFile("./uploads/files/" + filename)
            upload_file['title'] = name  # set the file name of this file
            upload_file.Upload()  # upload this file
        else:
            upload_file = drive.CreateFile()  # create the google drive file instance
            upload_file.SetContentFile("./uploads/files/" + filename)  # set our file into this instance
            upload_file['title'] = name  # set the file name of this file
            upload_file.Upload()  # upload this file
            permission = upload_file.InsertPermission({
                'type': 'anyone',
                'value': 'anyone',
                'role': 'reader'})
            google_file_id = upload_file[
                'id']  # can get this file's google drive-id and use it to save the id into database
            google_url = "https://drive.google.com/uc?authuser=0&id=" + google_file_id + "&export=download"
            User_question.add_user_question(user=current_user, question=this_question, record_url=google_url,
                                            record_id=google_file_id, record_title=name)  # save user_question to db

        os.remove("./uploads/files/" + filename)  # delete this file after uploading it to google drive
    return redirect(url_for('student_view', student_number=current_user.user_number))

def teacher_recorder():
    files = UploadSet('files', ALL)
    task_id_str = request.form.get("task_id")
    print(task_id_str)
    print(type(task_id_str))
    student_id_str = request.form.get("student_id")
    user_task = User_task.query.filter_by(task_id=task_id_str,
                                          user_id=student_id_str).one()
    print(user_task)
    if task_id_str:
        print(task_id_str)
        print(student_id_str)
        print(user_task)
        print(type(user_task))
        task_id = int(task_id_str)
        student_id = int(student_id_str)
        this_task = db.session.query(Task).filter(Task.id == task_id).one()
        this_student = db.session.query(User).filter(User.id == student_id).one()
        task_name = this_task.task_name
        student_number = this_student.user_number
        name = task_id_str + "_" + task_name + "_" + student_number + ".mp3"
        print(name)
    if request.method == 'POST' and 'upfile' in request.files:
        filename = files.save(
            request.files['upfile'])  # get the file from front end request, return the file name(String)
        if user_task.record_url:
            record_id = user_task.record_id
            print(record_id)
            upload_file = drive.CreateFile({'id': record_id})
            upload_file.SetContentFile("./uploads/files/" + filename)
            upload_file['title'] = name  # set the file name of this file
            upload_file.Upload()  # upload this file
        else:
            upload_file = drive.CreateFile()  # create the google drive file instance
            upload_file.SetContentFile("./uploads/files/" + filename)  # set our file into this instance
            upload_file['title'] = name  # set the file name of this file
            upload_file.Upload()  # upload this file
            permission = upload_file.InsertPermission({
                'type': 'anyone',
                'value': 'anyone',
                'role': 'reader'})
            google_file_id = upload_file[
                'id']  # can get this file's google drive-id and use it to save the id into database
            print(google_file_id)
            google_url = "https://drive.google.com/uc?authuser=0&id=" + google_file_id + "&export=download"
            print(google_url)
            user_task.record_url = google_url
            user_task.record_id = google_file_id
            user_task.record_title = name
            user_task.update()

        os.remove("./uploads/files/" + filename)  # delete this file after uploading it to google drive
    return redirect(url_for('teacher_view', staff_number=current_user.user_number))


def pdf_upload():
    files = UploadSet('files', ALL)
    task_id_str = request.form.get("task_id")
    if task_id_str:
        task_id = int(task_id_str)
        this_task = Task.query.filter_by(id=task_id).first()
    if request.method == 'POST' and 'file' in request.files:
        filename = files.save(
            request.files['file'])  # get the file from front end request, return the file name(String)
        if this_task.pdf_url:
            pdf_id = this_task.pdf_id
            upload_file = drive.CreateFile({'id': pdf_id})
            upload_file.SetContentFile("./uploads/files/" + filename)
            upload_file['title'] = filename  # set the file name of this file
            upload_file.Upload()  # upload this file
        else:
            upload_file = drive.CreateFile()  # create the google drive file instance
            upload_file.SetContentFile("./uploads/files/" + filename)  # set our file into this instance
            upload_file['title'] = filename  # set the file name of this file
            upload_file.Upload()  # upload this file
            permission = upload_file.InsertPermission({
                'type': 'anyone',
                'value': 'anyone',
                'role': 'reader'})
            google_file_id = upload_file[
                'id']  # can get this file's google drive-id and use it to save the id into database
            google_url = "https://drive.google.com/uc?authuser=0&id=" + google_file_id + "&export=download"
            this_task.pdf_url = google_url
            this_task.pdf_id = google_file_id
            this_task.update()
        os.remove("./uploads/files/" + filename)  # delete this file after uploading it to google drive
    flash("The PDF has been uploaded successfully.")
    return redirect(url_for('teacher_view', staff_number=current_user.user_number))


def task_result_downloader(task_id):
    # print(os.getcwd())
    path = os.getcwd() + "/recorder/csv/"
    # clear csv folder first to stop build up of files
    def empty_csv_folder():
        files = os.listdir(path)
        print("files = ", files)
        for f in files:
            print("f")
            if files.endswith(".csv"):
                print("removing")
                print("os.path.join(path, f) = ", os.path.join(path, f))
                os.remove(os.path.join(path, f))
    empty_csv_folder()
    results = User_task.query.filter_by(task_id=task_id)
    this_task = db.session.query(Task).filter(Task.id == task_id).one()
    filename = this_task.task_name + "_" + str(this_task.id) + ".csv"
    filepath = path + filename
    student_number = []
    first_name = []
    last_name = []
    mark = []
    for i in results:
        id = i.user_id
        student = db.session.query(User).filter(User.id == id).one()
        mark.append(i.mark)
        first_name.append(student.first_name)
        last_name.append(student.last_name)
        student_number.append(student.user_number)
    data = {'student_number': student_number,
            'first_name': first_name,
            'last_name': last_name,
            'mark': mark}
    df = DataFrame(data)
    columns = ['student_number', 'first_name', 'last_name', 'mark']
    df.to_csv(filepath, encoding="utf_8_sig", index=False, columns=columns)
    return send_from_directory(path, filename, as_attachment=True)  # as_attachment=True


def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswdResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(
                "You should soon receive an email allowing you to reset your \
                password. Please make sure to check your spam if you can't find the email."
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
    # print(user.first_name)
    if not user:
        return redirect(url_for('index'))
    form = PasswdResetForm()
    if form.validate_on_submit():
        user.set_password   (form.password.data)
        db.session.commit()
        flash("Congratulations. You have already reset your password !", "success")
        return redirect(url_for('index'))
    return render_template(
        'password_reset.html', title='Password Reset', form=form
    )




def page_404(e):
    return render_template('404.html'), 404

def page_500(e):
    return render_template('500.html'), 500
