from flask_restx import Resource, Namespace, reqparse
from ..models import User, Following
from ..api_models import follow_view_model
from ..extensions import db, api
from flask_login import current_user, login_required


friend_ns = Namespace("api", description='User operations')


# @login_required
# @friend_ns.route("/user/friends")
# class FriendApi(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('user_id', type=int, required=True,
#                         help='User ID is required in the request body')

#     @api.doc(description="Get all friends of logged in user.")
#     @friend_ns.marshal_list_with(follow_view_model)
#     @api.expect(parser, validate=True)
#     def get(self):
#         id = self.parser.parse_args()['user_id']
#         friends = []
#         ids = Following.query.filter_by(user_id=id).all()
#         for curr_id in ids:
#             friends.append(User.query.get(
#                 curr_id.followed_id))
#         return ids


# @login_required
# @friend_ns.route("/user/add_friend")
# class FriendAddApi(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('user_id', type=int, required=True,
#                         help='User ID is required in the request body')
#     parser.add_argument('new_friend_id', type=int, required=True,
#                         help='User ID is required in the request body')

#     @friend_ns.doc(description="Friend a user by thier id.")
#     def post(self):
#         curr_id = self.parser.parse_args()['user_id']
#         friend_id = self.parser.parse_args()['new_friend_id']

#         friend_user = User.query.get(friend_id)
#         # check user is not already friends
#         if friend_user is None:
#             return {"message": "Invalid friend."}, 400

#         friend_list = FriendApi.get()
#         if friend_user.id in friend_list:
#             return {"message": "Friend already exists"}, 400

#         if friend_user.id != current_user.id:
#             friend_relationship = Following(
#                 user_id=current_user.id, followed_id=friend_user.id)
#             db.session.add(friend_relationship)
#             db.session.commit()
#             return {"message": "Friend added."}, 200


# @login_required
# @friend_ns.route("/user/<int:id>/remove_friend")
# class FriendRemoveApi(Resource):
#     @login_required
#     @friend_ns.doc(description="Remove friend by thier id.")
#     def delete(self, id):
#         friend_user = User.query.get(id)
#         # check user is not already friends
#         if friend_user is not None and friend_user.id != current_user.id:
#             friend = Following.query.filter_by(
#                 user_id=current_user.id, followed_id=friend_user.id).first()

#             if friend:
#                 db.session.delete(friend)
#                 db.session.commit()
#                 return {"message": "Friend deleted."}, 200
#             else:
#                 return {"message": "Friend not found."}, 404
#         else:
#             return {"message": "Invalid Friend"}, 404
