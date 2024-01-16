from flask_restx import Resource, Namespace
from ..models import User
from ..api_models import user_input_model, user_login_model, user_resp_model
from ..extensions import db, bcrypt, api, jwt
import re
# from flask_login import login_user, login_required, logout_user, current_user

auth_ns = Namespace("api")  # essentially /api


def check_email_format(email):
    regex = r'\b[a-z0-9._%+-]+@[a-z.-]+\.[a-z]{2,7}\b'
    if (re.fullmatch(regex, email)):
        return True
    return False


@auth_ns.marshal_with(user_resp_model)
def return_user(user):
    return user, 200


@auth_ns.route("/login")
class UserLogin(Resource):
    @auth_ns.expect(user_login_model)
    @api.doc(description="Login the user.")
    def post(self):

        user = User.query.filter_by(email=auth_ns.payload["email"]).first()

        if user is not None:
            if (bcrypt.check_password_hash(user.password, auth_ns.payload["password"])):
                # login_user(user, remember=True)
                msg = "Login successfull."
                print(msg)
                return return_user(user)
            else:
                msg = "Password is incorrect."
                print(msg)
                return {'message': msg}, 400
        else:
            msg = "Acccount does not exist."
            print(msg)
            return {'message': msg}, 400


@auth_ns.route("/logout")
class UserLogout(Resource):
    # @login_required
    def get(self):
        # logout_user()
        msg = "Logout successfull."
        print(msg)
        return {'message': msg}, 200


@auth_ns.route("/signup")
class UserSignup(Resource):
    @auth_ns.expect(user_input_model)
    @api.doc(description="Sign up the user.")
    def post(self):
        # verify email exists, if valid
        user = User.query.filter_by(email=auth_ns.payload["email"]).first()
        if user:
            return {"message":  "User already exists."}, 400
        elif len(auth_ns.payload["name"]) <= 2:
            return {"message":  "Name is too short."}, 400
        elif len(auth_ns.payload["name"]) > 25:
            return {"message":  "Name is too long."}, 400
        elif not check_email_format(auth_ns.payload["email"]):
            return {"message":  "Email is not valid"}, 400
        elif len(auth_ns.payload["password"]) < 6:
            return {"message":  "Password is too short."}, 400
        elif len(auth_ns.payload["password"]) > 20:
            return {"message":  "Password is too long."}, 400
        else:
            hashed_pass = bcrypt.generate_password_hash(
                auth_ns.payload["password"]).decode('utf-8')
            new_user = User(email=auth_ns.payload["email"],
                            name=auth_ns.payload["name"],
                            password=hashed_pass)
            db.session.add(new_user)
            db.session.commit()
            msg = "Sign up succesfull."
            print(msg)
            return {'message': msg}, 201
