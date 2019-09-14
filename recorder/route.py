from flask import render_template, redirect, url_for, flash, request

from recorder import db
from recorder.forms import LoginForm, RegisterForm
from recorder.models.student import Student, student_unit_association
# student_task_association
from recorder.models.teacher import Teacher
from flask_login import login_user, current_user, logout_user, login_required
from recorder.models.comment import Comment
from recorder.models.question import Question
from recorder.models.unit import Unit
from recorder.models.record import Record
from recorder.models.task import Task
from recorder.models.student_question_association import StudentQuestionAssociation
from recorder.models.student_task_association import StudentTaskAssociation


# index
def index():
    if current_user.is_authenticated:
        return redirect(url_for("student_view"))          # after student, teacher finish, redirect to their pages
    form = LoginForm()
    if form.validate_on_submit():
        # print(form.username.data)
        student = Student.query.filter_by(student_number=form.username.data).first()
        teacher = Teacher.query.filter_by(staff_number=form.username.data).first()
        if student is not None and student.check_password(form.password.data):
            login_user(student, remember=form.remember_me.data)
            return redirect(url_for('student_view', username=student.student_number))
        if teacher is not None and teacher.check_password(form.password.data):
            login_user(teacher, remember=form.remember_me.data)
            return redirect(url_for('teacher_view'))
        else:
            flash("Invalid username or password, please try again.")
            # return redirect(url_for('index'))
    return render_template('index.html', title="Index", form=form)

@login_required
def student_view(username):
    student = Student.query.filter_by(student_number=username).first()
    return render_template('student_view.html', student=student)

@login_required
def teacher_view():
    return render_template('teacher_view.html')


# logout function
def logout():
    logout_user()
    return redirect(url_for('index'))


# register function
def register():

    form = RegisterForm()
    if form.validate_on_submit():
        student = Student(student_number=form.username.data,
                          first_name=form.firstname.data,
                          last_name=form.lastname.data,
                          email=form.email.data)
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', title='Registration', form=form)


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
