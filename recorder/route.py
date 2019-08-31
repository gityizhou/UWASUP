from flask import render_template
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
    output = "Hello guys"
    return render_template("index.html", output=output)


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
