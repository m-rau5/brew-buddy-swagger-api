from flask_restx import Resource, Namespace, reqparse, marshal
from ..models import User
from ..api_models import user_model, user_input_model, error_fields, user_resp_model
from ..extensions import db, api
# from .script import getTeas  -> used to insert ALL teas for the first time

users_ns = Namespace("api")


@users_ns.route("/users")
class UserList(Resource):
    @api.doc(description="Get list of all users.")
    @users_ns.marshal_list_with(user_model)
    def get(self):
        return User.query.all()


@users_ns.route("/user")
class UserApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, required=True,
                        help='The id of the user.')

    @api.doc(description="Get a user by thier id.")
    @api.expect(parser, validate=True)
    def get(self):
        id = self.parser.parse_args()['user_id']
        user = User.query.get(id)
        if user:
            return marshal(user, user_resp_model), 200
        else:
            return marshal({"message": "User does not exist."}, error_fields), 400


@users_ns.route("/user/update")
class LoggedInUserAPI(Resource):

    @api.doc(description="Lets a user update thier data. (empty fields are not changed)")
    @users_ns.expect(user_model)
    def put(self):
        id = users_ns.payload["id"]
        print(id)
        user = User.query.get(id)
        if not user:
            return marshal({"message": "User does not exist."}, error_fields), 400
        if users_ns.payload["name"]:
            user.name = users_ns.payload["name"]
        if users_ns.payload["email"]:
            user.email = users_ns.payload["email"]
        db.session.commit()
        return marshal(user, user_model), 200
