from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_uploads import UploadSet, ALL
from flask_login import login_user, current_user, logout_user, login_required
import sys

from recorder.forms import LoginForm, RegisterForm, SubscribeUnitForm, MakeTeacherForm, DeleteUserForm
from recorder.forms import DeleteUnitForm
from recorder.models.user import User
from recorder.models.unit import Unit
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
    form_make_teacher = MakeTeacherForm()
    form_delete_user = DeleteUserForm()
    form_delete_unit = DeleteUnitForm()
    if form_make_teacher.validate_on_submit():
        user = User.query.filter_by(user_number=form_make_teacher.userNumber.data).first()
        user.student2teacher()
        flash('The user now has teacher privileges.')
    if form_delete_user.validate_on_submit():
        user = User.query.filter_by(user_number=form_delete_user.userNumber.data).first()
        user.delete()
        flash('The user has been deleted.')
    if form_delete_unit.validate_on_submit():
        unit = Unit.query.filter_by(id=form_delete_unit.unitID.data).first()
        unit.delete()
        flash('The unit has been deleted.')
    teacher_units = teacher.units.all()
    all_units = Unit.query.all()
    all_users = User.query.all()
    return render_template('teacher_view.html', teacher=teacher, teacher_units=teacher_units, all_units=all_units,
                           all_users=all_users, form_make_teacher=form_make_teacher, form_delete_user=form_delete_user,
                           form_delete_unit=form_delete_unit)


# logout function
def logout():
    logout_user()
    return redirect(url_for('index'))


# register function
def register():
    # get the register form object
    form = RegisterForm()
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
        return redirect(url_for('index'))
    return render_template('register.html', title='Registration', form=form)


# recorder upload function, the folder now is default /uploads/files/
def upload():
    files = UploadSet('files', ALL)
    if request.method == 'POST' and 'upfile' in request.files:
        filename = files.save(request.files['upfile'])
        url = files.url(filename)
    return render_template('recorder.html')

