from flask_restx import fields
from .extensions import api


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


user_model = api.model("User",
                       {
                           "id": fields.Integer,
                           "name": fields.String,
                           "email": fields.String,
                           "password": fields.String,
                       })

user_input_model = api.model("UserInput",
                             {
                                 "name": fields.String,
                                 "email": fields.String,
                                 "password": fields.String
                             })

user_resp_model = api.model("UserResp",
                            {
                                "id": fields.Integer,
                                "name": fields.String,
                                "email": fields.String
                            })

user_login_model = api.model("UserLogin",
                             {
                                 "email": fields.String,
                                 "password": fields.String
                             })


follow_model = api.model("Firend",
                         {
                             "id": fields.Integer,
                             "user_id": fields.Integer,
                             "followed_id": fields.Integer
                         })

follow_update_model = api.model("Firend",
                                {
                                    "user_id": fields.Integer,
                                    "followed_id": fields.Integer
                                })

follow_view_model = api.model("Firend",
                              {
                                  "followed_id": fields.Integer
                              })
