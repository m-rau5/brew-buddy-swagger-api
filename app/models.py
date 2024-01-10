from .extensions import db
from flask_login import UserMixin

# TO CREATE: we can use: "flask shell" -> "from app.models import *"" -> "db.create_all()"" to create the db
# TO VIEW: we can use -> "sqlite3 instance/db.sqlite3" -> ".tables" to see the status of tables


class Following(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref(
        'user_relationships', lazy='dynamic'))
    followed_user = db.relationship('User', foreign_keys=[followed_id])


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(20))

    favourite_teas = db.relationship('Tea', backref='favourite_owner', lazy=True,
                                     foreign_keys='Tea.favourite_owner_id')

    # Relationship defining the owned teas for a user
    owned_teas = db.relationship('Tea', backref='owner', lazy=True,
                                 foreign_keys='Tea.owner_id')

    related_users = db.relationship('Following',
                                    foreign_keys=[Following.user_id],
                                    backref=db.backref(
                                        'main_user', lazy='joined'),
                                    lazy='dynamic')


class Tea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tea_id = db.Column(db.String(5), db.ForeignKey('tea.id'))
    name = db.Column(db.String(50), unique=True)
    image = db.Column(db.String(50))
    ingredients = db.Column(db.String(50))
    type = db.Column(db.String(25))
    prep_method = db.Column(db.String(50))
    min_infuzion = db.Column(db.Integer)
    max_infuzion = db.Column(db.Integer)

    favourite_owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Foreign key reference to the User table for owned teas
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
