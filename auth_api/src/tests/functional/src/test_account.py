from http import HTTPStatus
import base64


def test_login(client_with_db, create_user):
    """
    Тестирование авторизации
    """
    login = create_user.login
    password = create_user.password
    my_str = ":".join((login, password)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    response = client_with_db.post("/v1/login", headers={"Authorization": "Basic " + credentials})
    assert response.status_code == HTTPStatus.OK


def test_login_no_valid_user(client_with_db, create_user):
    """
    Тестирование авторизации c неверным паролем
    """
    username = create_user.login
    password = "qwfqwfq"
    my_str = ":".join((username, password)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    response = client_with_db.post("/v1/login", headers={"Authorization": "Basic " + credentials})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_change_login(client_with_db, access_headers):
    """
    Тестирование изменения логина
    """
    new_login = "changed_login"
    response = client_with_db.post("/v1/change_login", data={"new_login": new_login}, headers=access_headers)
    assert response.status_code == HTTPStatus.OK
    new_login = "changed_login"
    response = client_with_db.post("/v1/change_login", data={"new_login": new_login}, headers=access_headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_change_password(client_with_db, access_headers):
    """
    Тестирование изменения пароля
    """
    new_password = "changed_password"
    response = client_with_db.post("/v1/change_password", data={"new_password": new_password}, headers=access_headers)
    assert response.status_code == HTTPStatus.OK
    response = client_with_db.post("/v1/change_password", data={"new_password": new_password}, headers=access_headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_history(client_with_db, access_headers, not_access_headers):
    """
    Тестирование истории входов
    """
    response = client_with_db.get("/v1/login_history", headers=access_headers)
    assert response.status_code == HTTPStatus.OK
    response = client_with_db.get("/v1/login_history", headers=not_access_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_logout(client_with_db, access_headers, not_access_headers):
    """
    Тестирование Logout
    """
    response = client_with_db.delete("/v1/logout", headers=access_headers)
    assert response.status_code == HTTPStatus.OK
    response = client_with_db.delete("/v1/logout", headers=not_access_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_refresh(client_with_db, refresh_headers, not_access_headers):
    """
    Тестирование refresh
    """
    response = client_with_db.get("/v1/refresh", headers=refresh_headers)
    assert response.status_code == HTTPStatus.OK
    response = client_with_db.get("/v1/refresh", headers=not_access_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_singup(client_with_db):
    """
    Тестирование регистрации
    """
    login = "test_signup"
    password = "qwerty"
    response = client_with_db.post("/v1/sign_up", data={"login": login, "password": password})
    assert response.status_code == HTTPStatus.OK
    response = client_with_db.post("/v1/sign_up", data={"login": login})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = client_with_db.post("/v1/sign_up", data={"password": password})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
