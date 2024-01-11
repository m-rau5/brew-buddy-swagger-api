from flask_restx import Resource, Namespace
from ..models import User
from ..api_models import user_input_model, user_login_model
from ..extensions import db, api, bcrypt
from flask import abort
import re
from flask_login import login_user, login_required, logout_user, current_user

auth_ns = Namespace("api")  # essentially /api


def check_email_format(email):
    regex = r'\b[a-z0-9._%+-]+@[a-z.-]+\.[a-z]{2,7}\b'
    if (re.fullmatch(regex, email)):
        return True
    return False


@auth_ns.route("/login")
class UserLogin(Resource):
    @auth_ns.expect(user_login_model)
    @api.doc(description="Login the user.")
    def post(self):

        if current_user.is_authenticated:
            return {"message": "User already logged in."}, 401

        user = User.query.filter_by(email=auth_ns.payload["email"]).first()

        if user is not None:
            if (bcrypt.check_password_hash(user.password, auth_ns.payload["password"])):
                login_user(user, remember=True)
                return {'message': 'Login successfull.'}, 200
            else:
                abort(400, "Password is incorrect.")
        else:
            abort(400, "Acccount does not exist.")


@auth_ns.route("/logout")
class UserLogout(Resource):
    @login_required
    def get(self):
        logout_user()
        return {'message': 'Logout successfull.'}, 200


@auth_ns.route("/signup")
class UserSignup(Resource):
    @auth_ns.expect(user_input_model)
    @api.doc(description="Sign up the user.")
    def post(self):

        if current_user.is_authenticated:
            return {"message": "User already logged in."}, 401

        # verify email exists, if valid
        user = User.query.filter_by(email=auth_ns.payload["email"]).first()
        if user:
            abort(400, "User already exists.")
        elif len(auth_ns.payload["name"]) <= 2:
            abort(400, "Name is too short.")
        elif len(auth_ns.payload["name"]) > 25:
            abort(400, "Name is too long.")
        elif not check_email_format(auth_ns.payload["email"]):
            abort(400, "Email is not valid")
        elif len(auth_ns.payload["password"]) < 6:
            abort(400, "Password is too short.")
        elif len(auth_ns.payload["password"]) > 20:
            abort(400, "Password is too long.")
        else:
            hashed_pass = bcrypt.generate_password_hash(
                auth_ns.payload["password"]).decode('utf-8')
            new_user = User(email=auth_ns.payload["email"],
                            name=auth_ns.payload["name"],
                            password=hashed_pass)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return {"message": "User created and logged in succesfully."}, 201
