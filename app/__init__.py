from flask import Flask
from .extensions import api, db, bcrypt, login_manager
from .resources.auth_routes import auth_ns
from .resources.tea_routes import tea_ns
from .resources.user_routes import users_ns
from .resources.friend_routes import friend_ns
from flask_cors import CORS

from .models import User


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = 'Ana are mere'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    api.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    api.add_namespace(auth_ns)
    api.add_namespace(users_ns)
    api.add_namespace(tea_ns)
    api.add_namespace(friend_ns)

    @login_manager.user_loader  # to tell flask how to look for users to login
    def load_user(id):
        # query.get, by default, looks for the primaty key
        return User.query.get(int(id))

    return app
