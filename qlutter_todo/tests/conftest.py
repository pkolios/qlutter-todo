import json
import os

import pytest

from qlutter_todo.app import create_app
from qlutter_todo.extensions import db as _db
from qlutter_todo.models.user import User


TESTDB = 'test_todo.db'
TESTDB_PATH = '/tmp/{}'.format(TESTDB)
TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI
    }
    app = create_app(__name__, settings_override)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TESTDB_PATH)

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.yield_fixture
def api_client(app, session):
    with app.test_client() as client:
        yield client


@pytest.yield_fixture
def client(api_client):
    yield Client(api_client)


class Client(object):
    content_type = 'application/json'

    def __init__(self, client):
        self.client = client

    def __getattr__(self, method):
        def wrapper(*args, **kwargs):
            args, kwargs = self._prepare_request(*args, **kwargs)
            return self._prepare_response(
                getattr(self.client, method)(*args, **kwargs))
        return wrapper

    def _prepare_request(self, *args, **kwargs):
        kwargs['content_type'] = self.content_type
        if kwargs.get('json'):
            kwargs['data'] = json.dumps(kwargs.pop('json'))
        return args, kwargs

    def _prepare_response(self, response):
        if response.data:
            response.json = json.loads(response.data)
        return response


@pytest.fixture(scope='function')
def user(request, session):
    password = 'password'
    user = User('test@example.org', password)
    user.save()

    def teardown():
        User.delete(user)

    request.addfinalizer(teardown)
    return user.email, password
