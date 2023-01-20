from http import HTTPStatus


def test_assign_role(client_with_db, access_headers, not_access_headers, create_user, create_role):
    """
    Тестирование присвоение роли юзеру
    """
    login = create_user.login
    role = create_role.name
    response = client_with_db.post("/v1/assign_role", json={"login": login, "role": role}, headers=access_headers)
    assert response.status_code == HTTPStatus.OK
    response = client_with_db.post("/v1/assign_role", json={"login": login}, headers=access_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = client_with_db.post("/v1/assign_role", json={"role": role}, headers=access_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = client_with_db.post("/v1/assign_role", json={"login": login, "role": role}, headers=not_access_headers)
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_detach_role(client_with_db, access_headers, not_access_headers, create_user, create_role):
    """
    Тестирование лишения юзера роли
    """
    login = create_user.login
    role = create_role.name
    response = client_with_db.delete("/v1/detach_role", json={"login": login, "role": role}, headers=access_headers)
    assert response.status_code == HTTPStatus.OK
    response = client_with_db.post("/v1/detach_role", json={"login": login}, headers=access_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = client_with_db.post("/v1/detach_role", json={"role": role}, headers=access_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = client_with_db.post("/v1/detach_role", json={"login": login, "role": role}, headers=not_access_headers)
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_users_roles(client_with_db, access_headers, create_user):
    """
    Тестирование вывода списка ролей юзера
    """
    username = create_user.login
    response = client_with_db.get("/v1/users_roles", json={"login": username}, headers=access_headers)
    assert response.status_code == HTTPStatus.OK


def test_users_roles_not_valid(client_with_db, not_access_headers, create_user):
    """
    Тестирование вывода списка ролей юзера при невалидном токене
    """
    username = create_user.login
    response = client_with_db.get("/v1/users_roles", json={"login": username}, headers=not_access_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
