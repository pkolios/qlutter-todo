from flask import jsonify

from qlutter_todo.extensions import spec
from qlutter_todo.models.todo import ToDoSchema
from qlutter_todo.models.user import UserSchema


def build_spec(app):
    app.test_request_context().push()

    spec.definition('Todo', schema=ToDoSchema)
    spec.definition('User', schema=UserSchema)

    with app.app_context():
        for key in app.view_functions:
            if key != 'static':
                spec.add_path(view=app.view_functions[key])

    @app.route("/spec")
    def apispec():
        return jsonify(spec.to_dict())

    return app
