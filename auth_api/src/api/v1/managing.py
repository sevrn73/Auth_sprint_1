from http import HTTPStatus
from flask import jsonify, request, make_response

from src.db.managing_service import (
    get_roles_by_user,
    detach_role_from_user,
    assign_role_to_user,
)
from src.db.roles_service import get_role_by_name
from src.db.account_service import get_user_by_login
from src.core.jwt_decorators import jwt_admin_required


@jwt_admin_required()
def user_roles():
    login = request.json.get('login', None)
    if not login:
        return make_response('Login is empty', HTTPStatus.UNAUTHORIZED)
    users_roles = get_roles_by_user(login)
    output = [role.name for role in users_roles]
    return jsonify(roles=output)


@jwt_admin_required()
def assign_role():
    login = request.json.get('login', None)
    role = request.json.get('role', None)
    if not role or not login:
        return make_response('Role or login is empty', HTTPStatus.UNAUTHORIZED)
    db_role = get_role_by_name(role)
    if not db_role:
        return make_response('Role does not exist', HTTPStatus.CONFLICT)
    user_db = get_user_by_login(login)
    if not user_db:
        return make_response('User does not exist', HTTPStatus.CONFLICT)
    assign_role_to_user(user_db, db_role)
    return jsonify(msg=f'Role {role} was assigned to user {login}')


@jwt_admin_required()
def detach_role():
    login = request.json.get('login', None)
    role = request.json.get('role', None)
    if not role or not login:
        return make_response('Role or login is empty', HTTPStatus.UNAUTHORIZED)
    db_role = get_role_by_name(role)
    if not db_role:
        return make_response('Role does not exist', HTTPStatus.CONFLICT)
    user_db = get_user_by_login(login)
    if not user_db:
        return make_response('User does not exist', HTTPStatus.CONFLICT)
    detach_role_from_user(user_db, db_role)
    return jsonify(msg=f'Role {role} was  detached from user {login}')
