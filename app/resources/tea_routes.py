from flask_restx import Resource, Namespace, reqparse
from ..models import Tea, User, FavouriteTeas, OwnedTeas
from ..api_models import tea_model, tea_input_model, favourite_list_model
from ..extensions import db, api
from flask import jsonify
# from tea_inserter.script import getTeas # -> used to insert ALL teas for the first time

tea_ns = Namespace("api")  # essentially /api


@tea_ns.route("/teas")
class TeaListApi(Resource):
    @tea_ns.marshal_list_with(tea_model)
    @api.doc(description="Returns a list of all teas.", tags="tea")
    def get(self):
        # getTeas()  # -> used to insert ALL teas for the first time
        return Tea.query.all()

    @tea_ns.expect(tea_input_model)
    @tea_ns.marshal_with(tea_model)
    @api.doc(description="Insert a tea into the Db.", tags="tea")
    def post(self):
        tea = Tea(tea_id=tea_ns.payload["tea_id"],
                  name=tea_ns.payload["name"],
                  image=tea_ns.payload["image"],
                  ingredients=tea_ns.payload["ingredients"],
                  type=tea_ns.payload["type"],
                  prep_method=tea_ns.payload["prep_method"],
                  min_infuzion=tea_ns.payload["min_infuzion"],
                  max_infuzion=tea_ns.payload["max_infuzion"],
                  )
        db.session.add(tea)
        db.session.commit()
        return tea, 201


@tea_ns.route("/tea")
class TeaGetAPI(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('tea_id', type=int, required=True,
                        help='The database id of the tea (required)')

    @api.doc(description="Get a tea by its database id.", tags="tea")
    @tea_ns.marshal_with(tea_model)
    @api.expect(parser, validate=True)
    def get(self):
        tea_id = self.parser.parse_args()['tea_id']
        tea = Tea.query.get(tea_id)
        return tea


@tea_ns.route("/tea/favourites")
class TeaGetFavsAPI(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, required=True,
                        help='The id of the user to list his/her favourite teas')

    @api.doc(description="Get the teas in the user's favourites list.", tags="tea")
    @api.expect(parser, validate=True)
    @api.marshal_list_with(tea_model)
    def get(self):
        user_id = self.parser.parse_args()['user_id']
        user_list = FavouriteTeas.query.filter_by(user_id=user_id).all()
        favourites_list = []
        for fav_tea in user_list:
            curr_id = fav_tea.tea_id
            curr_tea = Tea.query.get(curr_id)
            favourites_list.append(curr_tea)
        return favourites_list, 200


@tea_ns.route("/tea/favourites/edit")
class TeaEditFavsAPI(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('tea_id', type=int, required=True,
                        help='The database id of the tea.')
    parser.add_argument('user_id', type=int, required=True,
                        help='The id of the user whose list we want to add the tea to.')

    @api.doc(description="Favourite/unfavourite a tea by its database id.", tags="tea")
    @api.expect(parser, validate=True)
    def post(self):
        tea_id = self.parser.parse_args()['tea_id']
        user_id = self.parser.parse_args()['user_id']
        tea = Tea.query.get(tea_id)
        user = User.query.get(user_id)

        if tea:
            if not user:
                return {"message": "User not found"}, 400

            entry = FavouriteTeas.query.filter_by(
                user_id=user_id, tea_id=tea_id).first()

            if entry:
                return {"message": "Tea is already in this users favourites."}, 400
            else:
                fav_tea = FavouriteTeas(
                    user_id=user_id, tea_id=tea_id)
                db.session.add(fav_tea)
                db.session.commit()

            return {"message": "Tea added to favourites!"}, 201
        else:
            return {"message": "Tea not found"}, 400

    @api.doc(description="Unfavourite a tea by its database id.", tags="tea")
    @api.expect(parser, validate=True)
    def delete(self):
        tea_id = self.parser.parse_args()['tea_id']
        user_id = self.parser.parse_args()['user_id']
        tea = Tea.query.get(tea_id)
        user = User.query.get(user_id)

        if tea:
            if not user:
                return {"message": "User not found."}, 400

            entry = FavouriteTeas.query.filter_by(
                user_id=user_id, tea_id=tea_id).first()
            print(entry)

            if entry:
                db.session.delete(entry)
                db.session.commit()
                return {"message": "Tea removed from favourites!"}, 200
            else:
                return {"message": "Tea is not in user's favourites list."}, 400
        else:
            return {"message": "Tea not found."}, 400


@tea_ns.route("/tea/owned")
class TeaGetOwnedAPI(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, required=True,
                        help='The id of the user to list his/her owned teas.')

    @api.doc(description="Get the teas in the user's owned list.", tags="tea")
    @api.expect(parser, validate=True)
    @api.marshal_list_with(tea_model)
    def get(self):
        user_id = self.parser.parse_args()['user_id']
        user_list = OwnedTeas.query.filter_by(user_id=user_id).all()
        owned_list = []
        for tea in user_list:
            curr_id = tea.tea_id
            curr_tea = Tea.query.get(curr_id)
            owned_list.append(curr_tea)
        return owned_list, 200


@tea_ns.route("/tea/owned/edit")
class TeaEditOwnedAPI(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('tea_id', type=int, required=True,
                        help='The database id of the tea.')
    parser.add_argument('user_id', type=int, required=True,
                        help='The id of the user whose owned list we want to add the tea to.')

    @api.doc(description="Add a tea to owned list by its database id.", tags="tea")
    @api.expect(parser, validate=True)
    def post(self):
        tea_id = self.parser.parse_args()['tea_id']
        user_id = self.parser.parse_args()['user_id']
        tea = Tea.query.get(tea_id)
        user = User.query.get(user_id)
        if tea:
            if not user:
                return {"message": "User not found"}, 400

            entry = OwnedTeas.query.filter_by(
                user_id=user_id, tea_id=tea_id).first()

            if entry:
                return {"message": "Tea is already in this users owned."}, 400
            else:
                fav_tea = OwnedTeas(
                    user_id=user_id, tea_id=tea_id)
                db.session.add(fav_tea)
                db.session.commit()

            return {"message": "Tea added to owned!"}, 201
        else:
            return {"message": "Tea not found"}, 400

    @api.doc(description="Remove a tea from owned list by its database id.", tags="tea")
    @api.expect(parser, validate=True)
    def delete(self):
        tea_id = self.parser.parse_args()['tea_id']
        user_id = self.parser.parse_args()['user_id']
        tea = Tea.query.get(tea_id)
        user = User.query.get(user_id)
        if tea:
            if not user:
                return {"message": "User not found."}, 400

            entry = OwnedTeas.query.filter_by(
                user_id=user_id, tea_id=tea_id).first()
            print(entry)

            if entry:
                db.session.delete(entry)
                db.session.commit()
                return {"message": "Tea removed from owned!"}, 200
            else:
                return {"message": "Tea is not in user's owned list."}, 400
        else:
            return {"message": "Tea not found."}, 400


@tea_ns.route("/tea/owned_favourites")
class TeaGetBothAPI(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, required=True,
                        help='The id of the user to list his/her owned teas.')

    @api.doc(description="Get the teas that are both in the user's owned and favorites list.", tags="tea")
    @api.expect(parser, validate=True)
    @api.marshal_list_with(tea_model)
    def get(self):
        user_id = self.parser.parse_args()['user_id']
        user_owned_list = OwnedTeas.query.filter_by(user_id=user_id).all()
        user_fav_list = FavouriteTeas.query.filter_by(user_id=user_id).all()
        # both_list = list(
        #     set(user_fav_list).intersection(user_owned_list))
        both_list = []
        for owned in user_owned_list:
            for fav in user_fav_list:
                if owned.tea_id == fav.tea_id:
                    both_list.append(Tea.query.get(owned.tea_id))

        return both_list, 200
