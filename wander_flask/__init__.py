from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from wander_flask.config import Config
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()
marsh = Marshmallow()
jwt = JWTManager()


def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    db.init_app(app=app)
    bcrypt.init_app(app=app)
    migrate.init_app(app=app,db=db)
    login_manager.init_app(app=app)
    mail.init_app(app=app)
    marsh.init_app(app=app)
    jwt.init_app(app=app)

    from wander_flask.main.routes import main
    from wander_flask.users.routes import users
    from wander_flask.posts.routes import posts
    from wander_flask.api.api import api
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(api)

    return app
