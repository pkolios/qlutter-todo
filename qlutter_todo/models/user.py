from marshmallow import Schema, fields

from qlutter_todo.models import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email()
