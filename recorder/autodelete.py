from recorder.models.task import Task
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
            t = str(sub.update_time)[:10]
            t = datetime.strptime(t, '%Y-%m-%d')
            if sub.update_time < one_month_ago:
                file_id = sub.record_id
                file = route.drive.CreateFile({'id': file_id})
                file.Delete()
                sub.record_url = 'deleted'
                sub.record_id = None
                sub.record_title = None
                sub.update()
                print("file deleted")
    #all_tasks = Task.query.all()
    #for record in all_tasks:
    #    print(record)
