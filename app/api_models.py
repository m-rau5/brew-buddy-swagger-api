from .extensions import api
from flask_restx import fields

tea_model = api.model("Tea",
                      {
                          "id": fields.Integer,
                          "tea_id": fields.String,
                          "name": fields.String,
                          "image": fields.String,
                          "ingredients": fields.String,
                          "type": fields.String,
                          "prep_method": fields.String,
                          "min_infuzion": fields.Integer,
                          "max_infuzion": fields.Integer
                          #   "course": fields.Nested(course_model)
                      })


user_model = api.model("User",
                       {
                           "id": fields.Integer,
                           "name": fields.String,
                           "email": fields.String,
                           "password": fields.String,
                           "favourite_teas": fields.List(fields.Nested(tea_model)),
                           "owned_teas": fields.List(fields.Nested(tea_model))
                       })

user_input_model = api.model("UserInput",
                             {
                                 "name": fields.String,
                                 "email": fields.String,
                                 "password": fields.String
                             })

user_login_model = api.model("UserLogin",
                             {
                                 "email": fields.String,
                                 "password": fields.String
                             })

tea_input_model = api.model("TeaInput",
                            {
                                "tea_id": fields.String,
                                "name": fields.String,
                                "image": fields.String,
                                "ingredients": fields.String,
                                "type": fields.String,
                                "prep_method": fields.String,
                                "min_infuzion": fields.Integer,
                                "max_infuzion": fields.Integer
                            })
