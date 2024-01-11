from flask_restx import Resource, Namespace
from ..models import User, Following
from ..api_models import follow_update_model
from ..extensions import db, api
from flask_login import current_user, login_required


friend_ns = Namespace("api")


@login_required
@friend_ns.route("/user/friends")
class FriendApi(Resource):
    @api.doc(description="Friend a user by its id.")
    def get(self):
        print(current_user)
        return Following.query.filter_by(user_id=current_user.id).all()


@login_required
@friend_ns.route("/user/<int:id>/friend")
class FriendAddApi(Resource):
    @api.doc(description="Friend a user by its id.")
    def get(self, id):
        friend_id = User.query.get(id)
        if friend_id is not None:
            friend_relaltionship = Following(user_id=current_user.id,
                                             followed_id=friend_id)
            db.session.add(friend_relaltionship),
            db.session.commit()
        return {"message": "Friend added."}, 200


# @login_required
# @friend_ns.route("/user/<int:id>/unfriend")
# class FriendApi(Resource):
#     @api.doc(description="Unfriend a user by its id.")
#     def get(self, id):
#         user = User.query.get(id)
#         return user, 200
