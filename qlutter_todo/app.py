import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from qlutter_todo.resources import todo, auth
from qlutter_todo.auth.utils import (
    authenticate, identity, auth_response_handler)
from qlutter_todo.extensions import db, bcrypt


def create_app(package_name, settings_override=None):
    app = Flask(package_name)
    app_root = os.path.dirname(os.path.abspath(__file__))
    app.config.from_pyfile(os.path.join(app_root, 'application.cfg'))
    if settings_override is not None:
        app.config.update(settings_override)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWT(app, authenticate, identity)
    jwt.auth_response_callback = auth_response_handler
    api = Api(app, catch_all_404s=True)

    # /auth endpoint is reserved by flask_jwt automatically
    api.add_resource(auth.Register, '/register')
    api.add_resource(auth.Logout, '/logout')
    api.add_resource(todo.TodoList, '/todos')
    api.add_resource(todo.Todo, '/todos/<int:todo_id>')
    return app


if __name__ == '__main__':
    app = create_app(__name__)
    with app.app_context():
        db.create_all()  # TODO: Remove that
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))
