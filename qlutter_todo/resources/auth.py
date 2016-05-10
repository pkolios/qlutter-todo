from flask import request
from flask_restful import abort, Resource
from flask_jwt import current_identity

from qlutter_todo.auth.utils import auth_required, logout
from qlutter_todo.models.user import User, UserSchema, UserAlreadyExists

user_schema = UserSchema()


class Register(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            abort(400, message='No input data provided')
        data, errors = user_schema.load(json_data)
        if errors:
            abort(422, **errors)
        user = User(**data)
        try:
            user.save()
        except UserAlreadyExists:
            abort(400, message='User already exists')
        data, errors = user_schema.dump(User.get_by_id(user.id))
        return data, 201


class Logout(Resource):
    decorators = [auth_required]

    def post(self):
        logout(current_identity)
        return {'message': 'Logout successfull'}, 200
