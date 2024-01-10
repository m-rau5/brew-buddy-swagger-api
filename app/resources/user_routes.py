from flask_restx import Resource, Namespace
from ..models import User
from ..api_models import tea_model, user_model, tea_input_model, user_input_model, user_login_model
from ..extensions import db, api
from flask import abort
# from .script import getTeas  -> used to insert ALL teas for the first time

ns2 = Namespace("api")  # essentially /api


@ns2.route("/users")
class UserList(Resource):
    @api.doc(description="Get list of all users.")
    @ns2.marshal_list_with(user_model)
    def get(self):
        return User.query.all()


@ns2.route("/user/<int:id>")
class UserApi(Resource):
    @api.doc(description="Get a user by its id.")
    @ns2.marshal_with(user_model)
    def get(self, id):
        user = User.query.get(id)
        return user, 200

    @api.doc(description="Update a user by its id.")
    @ns2.expect(user_input_model)
    @ns2.marshal_with(user_model)
    def put(self, id):
        user = User.query.get(id)
        user.name = ns2.payload["name"]
        user.course_id = ns2.payload["course_id"]
        db.session.commit()
        return user, 200

    @api.doc(description="Delete a user by its id.")
    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return {}, 204
