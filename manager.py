# manage.py
from flask_script import Manager
from flask_migrate import MigrateCommand
from recorder import create_app

# get the application instance
app = create_app()
# use flask script to manage our app
manager = Manager(app)
# migrate command to manage database
manager.add_command('db', MigrateCommand)

"""
main entry of our application, can manage ip address here
To run this application, please input:
python manager.py runserver
in your command line

python manager.py runserver -d
is debugging mode
"""

if __name__ == "__main__":
    manager.run()
