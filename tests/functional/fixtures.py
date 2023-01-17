import base64

import pytest
from flask_sqlalchemy import SQLAlchemy

from auth_api.src.app import create_app
from testdata.models import User, LoginHistory, Roles, UsersRoles
from utils.settings import TEST_SETTINGS


db = SQLAlchemy()


@pytest.fixture()
def app():

    app = create_app()
    app.config.update(
        {
            "SQLALCHEMY_DATABASE_URI": f"postgresql://{TEST_SETTINGS.posgres_name}:{TEST_SETTINGS.posgres_password}@{TEST_SETTINGS.db_url}/{TEST_SETTINGS.posgres_name}"
        }
    )
    app.config.update(
        {"TESTING": True,}
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def app_with_db(app):
    db.init_app(app)
    app.app_context().push()
    db.create_all()

    yield app
    db.drop_all()
    db.session.remove()


@pytest.fixture()
def client_with_db(app_with_db):
    return app_with_db.test_client()


@pytest.fixture()
def create_role():
    test_role = Roles(name="test_role")
    db.session.add(test_role)
    db.session.commit()
    return test_role


@pytest.fixture()
def create_user():
    test_user = User(login="test_user", pasword="qwerty")
    test_role = Roles(name="test")
    db.session.add(test_user)
    db.session.add(test_role)
    db.session.commit()
    new_assignment = UsersRoles(user_id=test_user.id, role_id=test_role.id)
    db.session.add(new_assignment)
    db.session.commit()

    return test_user


@pytest.fixture()
def token_response(create_user, client_with_db):
    user = create_user.login
    password = create_user.password
    my_str = ":".join((user, password)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    response = client_with_db.post("/v1/login", headers={"Authorization": "Basic " + credentials})
    return response


@pytest.fixture()
def access_headers(token_response):
    access_token = token_response.json.get("access_token")
    headers = {"Authorization": "Bearer " + access_token}
    return headers


@pytest.fixture()
def not_access_headers():
    login = "not_user"
    password = "not_password"
    my_str = ":".join((login, password)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    access_token = credentials
    headers = {"Authorization": "Bearer " + access_token}
    return headers


@pytest.fixture()
def refresh_headers(token_response):
    refresh_token = token_response.json.get("refresh_token")
    headers = {"Authorization": "Bearer " + refresh_token}
    return headers
