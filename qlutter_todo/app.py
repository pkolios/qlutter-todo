from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from qlutter_todo.resources import todo, auth
from qlutter_todo.auth.utils import (
    authenticate, identity, auth_response_handler)
from qlutter_todo.extensions import db, bcrypt

app = Flask(__name__)
app.config.from_pyfile('application.cfg')
db.init_app(app)
bcrypt.init_app(app)
jwt = JWT(app, authenticate, identity)
jwt.auth_response_callback = auth_response_handler
api = Api(app)

# /auth endpoint is reserved by flask_jwt automatically
api.add_resource(auth.Register, '/register')
api.add_resource(auth.Logout, '/logout')
api.add_resource(todo.TodoList, '/todos')
api.add_resource(todo.Todo, '/todos/<int:todo_id>')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # TODO: Remove that
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))