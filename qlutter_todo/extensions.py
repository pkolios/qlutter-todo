from apispec import APISpec
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

spec = APISpec(
    title='qlutter-todo',
    version='1.0.0',
    info=dict(
        description='A minimal TODO API'
    ),
    plugins=[
        'apispec.ext.flask',
        'apispec.ext.marshmallow'
    ]
)
