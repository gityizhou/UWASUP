web: gunicorn wsgi:app
gunicorn wsgi:app --timeout 60
init: python manager.py db init
migrate: python manager.py db migrate
release: python manager.py db upgrade
