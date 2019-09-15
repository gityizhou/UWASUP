from flask import render_template, redirect, url_for, flash

from recorder.forms import LoginForm, RegisterForm

from flask_login import login_user, current_user, logout_user, login_required
from recorder.models.user import User

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
    return render_template('student_view.html', student=student)


# After login, teacher will be redirected to this page
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
