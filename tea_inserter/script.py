import json
from app.extensions import db
from app.models import Tea

# Used for the first time insertion of the webscraped teas in the database


def getTeas():
    with open("tea_inserter/data_final.json", "r", encoding='utf-8') as file:
        jsFile = json.load(file)

    for elem in jsFile:
        tea = Tea(tea_id=elem["tea_id"],
                  name=elem["name"],
                  image=elem["image"],
                  ingredients=elem["ingredients"],
                  type=elem["type"],
                  prep_method=elem["prep_method"],
                  min_infuzion=elem["min_infuzion"],
                  max_infuzion=elem["max_infuzion"],
                  )
        db.session.add(tea)
        db.session.commit()
