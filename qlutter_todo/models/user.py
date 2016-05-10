from marshmallow import Schema, fields
from sqlalchemy.exc import IntegrityError

from qlutter_todo.extensions import bcrypt, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            raise UserAlreadyExists

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()

    def add_token(self, token):
        token = Token(token, self)
        token.save()

    def remove_token(self, token):
        token = Token.get_by_token(token)
        Token.delete(token)

    def verify_token(self, token):
        if Token.get_by_token(token):
            return True
        return False


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserAlreadyExists(Exception):
    pass


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User', backref=db.backref('tokens', lazy="dynamic"))

    def __init__(self, access_token, user):
        self.access_token = access_token
        self.user = user

    @classmethod
    def get_by_token(cls, token):
        return cls.query.filter_by(access_token=token).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def delete(token):
        db.session.delete(token)
        db.session.commit()
