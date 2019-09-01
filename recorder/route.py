from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required

from recorder.forms import LoginForm
from recorder.models.student import Student, student_unit_association
# student_task_association
from recorder.models.teacher import Teacher
from recorder.models.comment import Comment
from recorder.models.question import Question
from recorder.models.unit import Unit
from recorder.models.record import Record
from recorder.models.task import Task
from recorder.models.student_question_association import StudentQuestionAssociation
from recorder.models.student_task_association import StudentTaskAssociation


# index
def index():
    form = LoginForm()
    if form.validate_on_submit():
        # print(form.username.data)
        student = Student.query.filter_by(student_number=form.username.data).first()
        if student is None:
            if student is None or not student.check_password(form.password.data):
                print('invalid username or password')
                return redirect(url_for('index'))
            print('invalid username or password')
            return redirect(url_for('index'))
        return redirect(url_for('student_view'))
    return render_template('index.html', title="Index", form=form)


def student_view():
    return render_template('student_view.html')


def teacher_view():
    return render_template('teacher_view.html')


# login function
def login():
    pass


# logout function
def logout():
    pass


# register function
def register():
    pass


# forgot password
def forgot_password():
    pass


# download a record
def download_record(id):
    pass


# save a record
def save_record(id):
    pass


# assign tasks
def assign_tasks():
    pass


# delete tasks
def delete_tasks():
    pass


# upload function
def upload():
    pass


# download function
def download():
    pass


# show result
def show_result():
    pass
