from functools import wraps

from flask import current_app, jsonify
from flask_jwt import (
    _jwt_required, _default_request_handler, current_identity, JWTError)

from qlutter_todo.extensions import bcrypt
from qlutter_todo.models.user import User


def authenticate(email, password):
    user = User.get_by_email(email)
    if user and bcrypt.check_password_hash(user.password.encode('utf-8'),
                                           password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.get_by_id(user_id)


def auth_response_handler(access_token, user):
    access_token = access_token.decode('utf-8')
    user.add_token(access_token)
    return jsonify({'access_token': access_token})


def auth_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        _jwt_required(current_app.config['JWT_DEFAULT_REALM'])
        token = _default_request_handler()
        user = current_identity
        if not user.verify_token(token):
            raise JWTError('Bad request', 'Invalid token')
        return fn(*args, **kwargs)
    return decorator


def logout(user):
    token = _default_request_handler()
    user.remove_token(token)
