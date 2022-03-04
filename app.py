from refs import create_app

# no cover 3.x
# Call the application factory function to construct a Flask application
# instance using the development configuration
app = create_app("flask.cfg")
