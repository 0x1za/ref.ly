web: gunicorn refs.app:app
init: cd refs || flask db init
migrate: flask db migrate -m "Initial migration."
upgrade: flask db upgrade
