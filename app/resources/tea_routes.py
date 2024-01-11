from flask_restx import Resource, Namespace
from ..models import Tea
from ..api_models import tea_model, tea_input_model
from ..extensions import db, api
# from .script import getTeas  -> used to insert ALL teas for the first time

tea_ns = Namespace("api")  # essentially /api


@tea_ns.route("/teas")
class TeaListApi(Resource):
    @tea_ns.marshal_list_with(tea_model)
    @api.doc(description="Returns a list of all teas.", tags="tea")
    def get(self):
        # getTeas() -> used to insert ALL teas for the first time
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


@tea_ns.route("/tea/<int:id>")
class TeaAPI(Resource):
    @api.doc(description="Get a tea by its database id.", tags="tea")
    @tea_ns.marshal_with(tea_model)
    def get(self, id):
        tea = Tea.query.get(id)
        return tea

    @api.doc(description="Delete a tea by its database id.", tags="tea")
    def delete(self, id):
        tea = Tea.query.get(id)
        db.session.delete(tea)
        db.session.commit()
        return {}, 204


@tea_ns.route("/tea/<int:id>")
class TeaAPI(Resource):
    @api.doc(description="Get a tea by its database id.", tags="tea")
    @tea_ns.marshal_with(tea_model)
    def get(self, id):
        tea = Tea.query.get(id)
        return tea

    @api.doc(description="Delete a tea by its database id.", tags="tea")
    def delete(self, id):
        tea = Tea.query.get(id)
        db.session.delete(tea)
        db.session.commit()
        return {}, 204


# @login_required
# @tea_ns.route("/tea/<int:id>/favourite")
# class TeaAPI(Resource):
#     @api.doc(description="Favourite a tea by its database id.", tags="tea")
#     @tea_ns.marshal_with(tea_model)
#     def get(self, id):
#         tea = Tea.query.get(id)
#         user_id = current_user.id
#         user = User.query.get(id)

#         return tea

    @api.doc(description="Delete a tea by its database id.", tags="tea")
    def delete(self, id):
        course = Tea.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return {}, 204
