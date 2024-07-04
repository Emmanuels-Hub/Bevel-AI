from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from Ulo.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from Ulo.main.routes import main
    from Ulo.bevel.routes import bevel

    app.register_blueprint(main)
    app.register_blueprint(bevel)

    return app