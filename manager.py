# manage.py
from flask_script import Manager
from flask_migrate import MigrateCommand
from recorder import create_app

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)   # add migrate command to control db process

if __name__ == "__main__":
    app.run()