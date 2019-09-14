from flask import render_template, redirect, url_for, flash, request

from recorder import db
from recorder.forms import LoginForm, RegisterForm

# student_task_association

from flask_login import login_user, current_user, logout_user, login_required
from recorder.models.user import User
from recorder.models.unit import Unit
from recorder.models.task import Task
from recorder.models.question import Question
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
    if current_user.is_authenticated:
        if current_user.is_teacher == 1:
            return redirect(url_for('teacher_view', staff_number=current_user.user_number))
        if current_user.is_teacher == 0:
            return redirect(url_for('student_view', student_number=current_user.user_number))
    form = LoginForm()
    if form.validate_on_submit():
        # print(form.username.data)
        user = User.query.filter_by(user_number=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            if user.is_teacher == 1:
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('teacher_view', staff_number=current_user.user_number))
            if user.is_teacher == 0:
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('student_view', student_number=current_user.user_number))
        else:
            flash("Invalid username or password, please try again.")
            # return redirect(url_for('index'))
    return render_template('index.html', title="Index", form=form)


@login_required
def student_view(student_number):
    student = current_user
    return render_template('student_view.html', student=student)


@login_required
def teacher_view(staff_number):
    teacher = current_user
    return render_template('teacher_view.html', teacher=teacher)


# logout function
def logout():
    logout_user()
    return redirect(url_for('index'))


# register function
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(user_number=form.username.data,
                    first_name=form.firstname.data,
                    last_name=form.lastname.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', title='Registration', form=form)



