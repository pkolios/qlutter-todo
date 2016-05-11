from marshmallow import Schema, fields

from qlutter_todo.extensions import db
from qlutter_todo.models.user import UserSchema


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_on = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('todos', lazy="dynamic"))

    @classmethod
    def get_all(cls, user=None, filters=None):
        if not user and not filters:
            return cls.query.all()

        filters = filters or {}
        if user:
            filters['user'] = user
        return cls.query.filter_by(**filters)

    @classmethod
    def get_by_id(cls, todo_id, user=None):
        if user:
            return cls.query.filter_by(id=todo_id, user=user).first()
        return cls.query.get(todo_id)

    @staticmethod
    def create(todo, user=None):
        if user:
            todo.user = user
        db.session.add(todo)
        db.session.commit()

    @staticmethod
    def update(todo, data):
        for key in data:
            setattr(todo, key, data[key])
        db.session.add(todo)
        db.session.commit()

    @staticmethod
    def delete(todo):
        db.session.delete(todo)
        db.session.commit()


class ToDoSchema(Schema):
    id = fields.Int(dump_only=True)
    text = fields.Str(required=True)
    completed = fields.Boolean(missing=False)
    completed_on = fields.DateTime()
    user = fields.Nested(UserSchema, required=True, load_only=True)
