from flask_restx import Resource, Namespace
from ..models import User
from ..api_models import user_model, user_input_model
from ..extensions import db, api
from flask_login import login_required, current_user

# from .script import getTeas  -> used to insert ALL teas for the first time

users_ns = Namespace("api")


@users_ns.route("/users")
class UserList(Resource):
    @api.doc(description="Get list of all users.")
    @users_ns.marshal_list_with(user_model)
    def get(self):
        return User.query.all()


@users_ns.route("/user/<int:id>")
class UserApi(Resource):
    @api.doc(description="Get a user by thier id.")
    @users_ns.marshal_with(user_model)
    def get(self, id):
        user = User.query.get(id)
        return user, 200

    # @api.doc(description="Update a user by its id. (only name/email works)")
    # @users_ns.expect(user_input_model)
    # @users_ns.marshal_with(user_model)
    # def put(self, id):
    #     user = User.query.get(id)
    #     if users_ns.payload["name"]:
    #         user.name = users_ns.payload["name"]
    #     if users_ns.payload["email"]:
    #         user.email = users_ns.payload["email"]
    #     db.session.commit()
    #     return user, 200

    # @api.doc(description="Delete a user by thier id.")
    # def delete(self, id):
    #     user = User.query.get(id)
    #     db.session.delete(user)
    #     db.session.commit()
    #     return {}, 204


@users_ns.route("/user/update")
class LoggedInUserAPI(Resource):
    @api.doc(description="Lets a logged in user update thier data. (empty fields are not changed)")
    @users_ns.marshal_with(user_model)
    @users_ns.expect(user_input_model)
    @login_required
    def put(self):
        user = User.query.get(current_user.id)
        if users_ns.payload["name"]:
            user.name = users_ns.payload["name"]
        if users_ns.payload["email"]:
            user.email = users_ns.payload["email"]
        db.session.commit()
        return user, 200
