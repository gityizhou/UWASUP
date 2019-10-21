from recorder.models.user_task import User_task
from recorder.models.user_question import User_question
from datetime import datetime, timedelta
from recorder import route


def delete_old_recordings():
    one_month_ago = datetime.now() - timedelta(days=30)
    one_month_ago = str(one_month_ago)[:10]
    one_month_ago = datetime.strptime(one_month_ago, '%Y-%m-%d')
    all_submissions = User_question.query.all()
    for sub in all_submissions:
        if sub.update_time is not None:
            if sub.update_time < one_month_ago:
                file_id = sub.record_id
                file = route.drive.CreateFile({'id': file_id})
                file.Delete()
                sub.record_url = 'deleted'
                sub.record_id = None
                sub.record_title = None
                sub.update_time = None
                sub.update()
    all_user_tasks = User_task.query.all()
    for record in all_user_tasks:
        if record.record_create_time is not None:
            if record.record_create_time < one_month_ago:
                file_id = record.record_id
                file = route.drive.CreateFile({'id': file_id})
                file.Delete()
                record.record_url = 'deleted'
                record.record_id = None
                record.record_title = None
                record.record_create_time = None
                record.update()
    all_user_tasks = User_task.query.all()
