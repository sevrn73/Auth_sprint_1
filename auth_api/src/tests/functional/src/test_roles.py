from http import HTTPStatus


def test_create_role(client_with_db, access_headers):
    """
    Тестирование создания роли
    """
    new_role = "asfasfqwfqwfwasda"
    response = client_with_db.post("/v1/create_role", data={"new_role": new_role}, headers=access_headers)
    assert response.status_code == HTTPStatus.OK
    response = client_with_db.post("/v1/create_role", data={"new_role": new_role}, headers=access_headers)
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    response = client_with_db.post("/v1/create_role", data={"new_role": ""}, headers=access_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_role(client_with_db, create_role, access_headers):
    """
    Тестирование удаления роли
    """
    role = create_role.name
    response = client_with_db.delete("/v1/delete_role", data={"role": role}, headers=access_headers)
    assert response.status_code == HTTPStatus.OK
    response = client_with_db.delete("/v1/delete_role", data={"role": role}, headers=access_headers)
    assert response.status_code == HTTPStatus.CONFLICT


def test_rename_role(client_with_db, create_role, access_headers):
    """
    Тестирование изменение роли
    """
    role = create_role.name
    new_name = "asfasfasqwfqwf"
    response = client_with_db.put("/v1/rename_role", data={"role": role, "new_name": new_name}, headers=access_headers)
    assert response.status_code == HTTPStatus.OK
    not_valid_role = "not_role"
    response = client_with_db.put(
        "/v1/rename_role", data={"role": not_valid_role, "new_name": new_name}, headers=access_headers
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_roles_list(client_with_db, access_headers, not_access_headers):
    """
    Тестирование вывода списка ролей
    """
    response = client_with_db.get("/v1/roles_list", headers=access_headers)
    assert response.status_code == HTTPStatus.OK
    response = client_with_db.get("/v1/roles_list", headers=not_access_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
