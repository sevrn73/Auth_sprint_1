import sys
from os.path import dirname as d
from os.path import abspath, join
root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)

import base64

import pytest
from flask_sqlalchemy import SQLAlchemy

from app import create_app
# from src.tests.functional.testdata.models import User, LoginHistory, Roles, UsersRoles#, db
from src.tests.functional.utils.settings import TEST_SETTINGS
from pydantic import BaseSettings, Field
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
class DbSettings(BaseSettings):
    dbname: str = Field('postgres', env='POSTGRES_NAME')
    user: str = Field('postgres', env='POSTGRES_USER')
    password: str = Field('postgres', env='POSTGRES_PASSWORD')
    host: str = Field('db', env='DB_HOST')
    port: int = Field(5432, env='DB_PORT')

db_settings = DbSettings()

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<User {self.login}>"


class LoginHistory(db.Model):
    __tablename__ = "login_history"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id))
    user_agent = db.Column(db.String, nullable=False)
    auth_date = db.Column(db.DateTime, nullable=False)


class Roles(db.Model):
    __tablename__ = "roles"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Roles {self.name}>"


class UsersRoles(db.Model):
    """связь пользователя и роли.
    Одному пользователю может быть назначено несколько ролей """

    __tablename__ = "users_roles"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id))
    role_id = db.Column(UUID(as_uuid=True), ForeignKey(Roles.id))


@pytest.fixture()
def app():

    app = create_app()
    app.config.update(
        {
            "SQLALCHEMY_DATABASE_URI": f'postgresql://{db_settings.user}:{db_settings.password}@{":".join((db_settings.host, str(db_settings.port)))}/{db_settings.dbname}'#f"postgresql://{TEST_SETTINGS.posgres_name}:{TEST_SETTINGS.posgres_password}@{TEST_SETTINGS.db_url}/{TEST_SETTINGS.posgres_name}"
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


@pytest.fixture()
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
    # try:
    db.session.add(test_role)
    db.session.commit()
    # except:
    #     pass
    return test_role


@pytest.fixture()
def create_user():
    test_user = User(login="tt", password="qwertyttt")
    db.session.add(test_user)
    test_role = Roles(name="test_role")
    db.session.add(test_role)
    db.session.commit()
    new_assignment = UsersRoles(user_id=test_user.id, role_id=test_role.id)
    db.session.add(new_assignment)
    db.session.commit()
    # except:
    #     pass
    return test_user


@pytest.fixture()
def token_response(client_with_db, create_user):
    user = create_user.login
    password = create_user.password
    my_str = ":".join((user, password)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    response = client_with_db.post("/v1/login", headers={"Authorization": "Basic " + credentials})
    return response


@pytest.fixture()
def access_headers(token_response):
    access_token = token_response.json.get('access_token')
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
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
    refresh_token = token_response.json.get('refresh_token')
    headers = {
        'Authorization': 'Bearer ' + refresh_token
    }
    return headers

# def pytest_collection_modifyitems(items):
#     for item in items:
#         item.add_marker('asyncio')



