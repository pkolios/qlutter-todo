from flask import request
from flask_jwt import current_identity
from flask_restful import abort, Resource

from qlutter_todo.auth.utils import auth_required
from qlutter_todo.models.todo import ToDo, ToDoSchema


todo_schema = ToDoSchema()
todos_schema = ToDoSchema(many=True)


def todo_exists(f):
    """Checks whether todo exists or raises error 404."""
    def decorator(*args, **kwargs):
        if not ToDo.get_by_id(kwargs.get('todo_id'), current_identity):
            abort(404, message="Todo {} doesn't exist".format('todo_id'))
        return f(*args, **kwargs)
    return decorator


class Todo(Resource):
    decorators = [todo_exists, auth_required]  # Applied from right to left

    def get(self, todo_id):
        data, errors = todo_schema.dump(
            ToDo.get_by_id(todo_id, current_identity))
        return data, 200

    def delete(self, todo_id):
        todo = ToDo.get_by_id(todo_id, current_identity)
        ToDo.delete(todo)
        return {'message': 'Todo {} deleted'.format(todo_id)}, 200

    def put(self, todo_id):
        json_data = request.get_json(force=True)
        if not json_data:
            abort(400, message="No input data provided")
        data, errors = todo_schema.load(json_data, partial=('user',))
        if errors:
            abort(422, **errors)
        todo = ToDo.get_by_id(todo_id, current_identity)
        ToDo.update(todo, data)
        data, errors = todo_schema.dump(ToDo.get_by_id(todo.id))
        return data, 200


class TodoList(Resource):
    decorators = [auth_required]

    def get(self):
        data, errors = todos_schema.dump(ToDo.get_all(current_identity))
        return data, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            abort(400, message="No input data provided")
        data, errors = todo_schema.load(json_data, partial=('user',))
        if errors:
            abort(422, **errors)
        todo = ToDo(**data)
        ToDo.create(todo, current_identity)
        data, errors = todo_schema.dump(ToDo.get_by_id(todo.id))
        return data, 201
