from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'login'  # endpoint name for login

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login.init_app(app)

    # Import models and routes after extensions are initialized
    with app.app_context():
        import models  # noqa: F401
        import routes  # noqa: F401
        db.create_all()

    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    # Running directly for development; in production use a WSGI server.
    app.run(debug=True)