from http import HTTPStatus
from flask import jsonify, request, make_response

from db.roles_service import (
    create_role_db,
    delete_role_db,
    change_role_db,
)
from core.jwt_decorators import jwt_admin_or_manager_required


@jwt_admin_or_manager_required()
def create_role():
    role = request.values.get('new_role', None)
    if not role:
        return make_response('New role is empty', HTTPStatus.UNAUTHORIZED)

    new_role = create_role_db(role)
    return jsonify(msg=f'Role {role} was successfully created')


@jwt_admin_or_manager_required()
def delete_role():
    role = request.values.get('role', None)
    if not role:
        return make_response('Role is empty', HTTPStatus.UNAUTHORIZED)
    db_role = Roles.query.filter_by(name=role).first()
    if not db_role:
        return make_response('Role does not exist', HTTPStatus.CONFLICT)
    delete_role_db(db_role)
    return jsonify(msg=f'Role {role} was successfully deleted')


@jwt_admin_or_manager_required()
def change_role():
    role = request.values.get('role', None)
    new_role = request.values.get('new_name', None)
    if not role or not new_role:
        return make_response('Role or new name is empty', HTTPStatus.UNAUTHORIZED)

    change_role_db(role, new_role)
    return jsonify(msg=f'Role {role} was successfully changed')


@jwt_admin_or_manager_required()
def roles_list():
    roles = Roles.query.all()
    output = [role.name for role in roles]
    return jsonify(roles=output)
