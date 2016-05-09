from flask import Flask
from flask_restful import Api

from qlutter_todo import resources
from qlutter_todo.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db.init_app(app)
api = Api(app)

api.add_resource(resources.TodoList, '/todos')
api.add_resource(resources.Todo, '/todos/<int:todo_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # TODO: Remove that
    app.run(debug=True, host='0.0.0.0')
