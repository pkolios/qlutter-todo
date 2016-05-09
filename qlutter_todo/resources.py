from flask import request
from flask_restful import abort, Resource

from models.todo import ToDo, ToDoSchema


todo_schema = ToDoSchema()
todos_schema = ToDoSchema(many=True)


def todo_exists(f):
    """Checks whether todo exists or raises error 404."""
    def decorator(*args, **kwargs):
        if not ToDo.get_by_id(kwargs.get('todo_id')):  # TODO: get for user
            abort(404, message="Todo {} doesn't exist".format('todo_id'))
        return f(*args, **kwargs)
    return decorator


class Todo(Resource):
    decorators = [todo_exists]

    def get(self, todo_id):
        data, errors = todo_schema.dump(ToDo.get_by_id(todo_id))
        return data, 200

    def delete(self, todo_id):
        todo = ToDo.get_by_id(todo_id)
        ToDo.delete(todo)
        return {'message': 'Todo {} deleted'.format(todo_id)}, 200

    def put(self, todo_id):
        json_data = request.get_json(force=True)
        if not json_data:
            abort(400, message="No input data provided")
        data, errors = todo_schema.load(json_data)
        if errors:
            abort(422, **errors)
        todo = ToDo.get_by_id(todo_id)
        ToDo.update(todo, data)
        data, errors = todo_schema.dump(ToDo.get_by_id(todo.id))
        return data, 201


class TodoList(Resource):
    def get(self):
        # TODO: get all for user
        data, errors = todos_schema.dump(ToDo.get_all())
        return data, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            abort(400, message="No input data provided")
        data, errors = todo_schema.load(json_data)
        if errors:
            abort(422, **errors)
        todo = ToDo(**data)
        ToDo.create(todo)
        data, errors = todo_schema.dump(ToDo.get_by_id(todo.id))
        return data, 201
