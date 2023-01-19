from functools import wraps
from http import HTTPStatus
from flask import make_response
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request


def jwt_admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            token = get_jwt()
            if token['role'] == 'admin':
                return fn(*args, **kwargs)
            else:
                return make_response('Only administrators are allowed access', HTTPStatus.METHOD_NOT_ALLOWED)

        return decorator

    return wrapper


def jwt_admin_or_manager_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            token = get_jwt()
            if token['role'] in ['admin', 'manager']:
                return fn(*args, **kwargs)
            else:
                return make_response(
                    'Only administrators and managers are allowed access', HTTPStatus.METHOD_NOT_ALLOWED
                )

        return decorator

    return wrapper
