from http import HTTPStatus
from flask import jsonify, request, make_response

from db.managing_service import (
    get_roles_by_user,
    detach_role_from_user,
    assign_role_to_user,
)
from core.jwt_decorators import jwt_admin_required


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
    db_role = Roles.query.filter_by(name=role).first()
    if not db_role:
        return make_response('Role does not exist', HTTPStatus.CONFLICT)
    user_db = User.query.filter_by(login=login).first()
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
    db_role = Roles.query.filter_by(name=role).first()
    if not db_role:
        return make_response('Role does not exist', HTTPStatus.CONFLICT)
    user_db = User.query.filter_by(login=login).first()
    if not user_db:
        return make_response('User does not exist', HTTPStatus.CONFLICT)
    detach_role_from_user(user_db, db_role)
    return jsonify(msg=f'Role {role} was  detached from user {login}')
