# Professional Computing CITS5206 project
## Group Number CITS5206-3
This is a cool project for CITS5206 .

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

This application can be deployed locally. On linux, install git and clone the reposistory.

Get the code:
```
git clone https://github.com/zhouyi119119/CITS5206_Project
```
How to run from zip

Generate a virtual environment and install dependencies:
```
Unix:
$ python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Windows:
$ venv\Scripts\activate
(venv) $ _
pip install -r requirements.txt
```

set the FLASK_APP and FLASK_DEBUG variables
```
export FLASK_APP=CITS5206.py
export FLASK_DEBUG=1
```

Initialise database

```
flask db migrate
flask db upgrade
```

Start the application:
```
python manager.py runserver
Check if a poll already exists into db
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```


If you run the application with app.db and the current migrations, there are logins that
demonstrate the applications functionality.

### Coding style tests

HTML and CSS have been validated using w3schools validator:

```
https://validator.w3.org/#validate_by_uri
```

## Deployment

To deploy on Heroku, visit heroku.com and create a free account.
Once the CLI is installed is login to your Heroku account:

```
$ heroku login
```

HerokuCLI will ask you to enter your email address and your account password.
Git must be installed on your system for deployment.

To register a new application, use the apps:create command :
```
$ heroku apps:create Flask-poll-master
```

Change config log (config.py) and init (__init__.py) for application to log directly to standard output.
```
class Config(object):
    # ...
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
```
```
if app.config['LOG_TO_STDOUT']:
```
Set the LOG_TO_STDOUT environment variable when the application runs in Heroku:
```
$ heroku config:set LOG_TO_STDOUT=1
```

Create a file named Procfile in the root directory of the application:
```
web: flask db upgrade; flask translate compile; gunicorn Flask-poll-master:app
```
Add the FLASK_APP environment variable:
```
$ heroku config:set FLASK_APP=polling.py
```

Upload the application to Heroku's servers for deployment, using the git push command.
```
$ git checkout -b deploy
$ git push heroku deploy:master
```

```
$ git commit -a -m "heroku deployment changes"
```
Start the deployment:
```
$ git push heroku master
```

## Authors
 
* Team 5206_3
FirstName	  Surname       	Email
* Yi	      Zhou	          22302319@student.uwa.edu.au
* Zhaoyu	  Shang	          22540031@student.uwa.edu.au
* Yuran	    Li	            22314412@student.uwa.edu.au
* Dana	    Ahmadibroujeni	22427581@student.uwa.edu.au
* Alexandra	McAllister	    20358346@student.uwa.edu.au
* Amanpreet Kaur	          22325986@student.uwa.edu.au
