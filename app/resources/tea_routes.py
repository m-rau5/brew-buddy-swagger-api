from flask_restx import Resource, Namespace
from ..models import Tea, User
from flask import jsonify
from ..api_models import tea_model, user_model, tea_input_model, user_input_model, user_login_model
from ..extensions import db, api
from flask import abort
# from .script import getTeas  -> used to insert ALL teas for the first time

ns1 = Namespace("api")  # essentially /api


@ns1.route("/teas")
class TeaListApi(Resource):
    @ns1.marshal_list_with(tea_model)
    @api.doc(description="Returns a list of all teas.", tags="tea")
    def get(self):
        # getTeas() -> used to insert ALL teas for the first time
        return Tea.query.all()

    @ns1.expect(tea_input_model)
    @ns1.marshal_with(tea_model)
    @api.doc(description="Insert a tea into the Db.", tags="tea")
    def post(self):
        tea = Tea(tea_id=ns1.payload["tea_id"],
                  name=ns1.payload["name"],
                  image=ns1.payload["image"],
                  ingredients=ns1.payload["ingredients"],
                  type=ns1.payload["type"],
                  prep_method=ns1.payload["prep_method"],
                  min_infuzion=ns1.payload["min_infuzion"],
                  max_infuzion=ns1.payload["max_infuzion"],
                  )
        db.session.add(tea)
        db.session.commit()
        return tea, 201


@ns1.route("/tea/<int:id>")
class TeaAPI(Resource):
    @api.doc(description="Get a tea by its database id.", tags="tea")
    @ns1.marshal_with(tea_model)
    def get(self, id):
        course = Tea.query.get(id)
        return course

    # @ns1.expect(tea_input_model)
    # @ns1.marshal_with(tea_model)
    # @api.doc(description="Update a tea by it's id.")
    # def put(self, id):
    #     tea = Tea.query.get(id)
    #     tea.name = ns1.payload["name"]
    #     db.session.commit()
    #     return tea

    @api.doc(description="Delete a tea by its database id.", tags="tea")
    def delete(self, id):
        course = Tea.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return {}, 204
