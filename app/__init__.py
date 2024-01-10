from flask import Flask
from .extensions import api, db, bcrypt, login_manager
from .resources.auth_routes import ns
from .resources.tea_routes import ns1
from .resources.user_routes import ns2
from .models import User


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Ana are mere'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    api.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    api.add_namespace(ns)
    api.add_namespace(ns2)
    api.add_namespace(ns1)

    @login_manager.user_loader  # to tell flask how to look for users to login
    def load_user(id):
        # query.get, by default, looks for the primaty key
        return User.query.get(int(id))

    return app
