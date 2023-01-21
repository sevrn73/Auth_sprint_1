import os
import pytest
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import base64
import sys
from os.path import dirname as d
from os.path import abspath, join
root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)

load_dotenv()

TEST_LOGIN = 'test_login'
TEST_PASSWORD = 'test_password'
TEST_LOGIN_NEW = "changed_login"
TEST_PASSWORD_NEW = "changed_password"

@pytest.fixture(scope="function")
def user():
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/sign_up',
        data={'login': TEST_LOGIN, 'password': TEST_PASSWORD},
    )

    return response

@pytest.fixture(scope="function")
def token_response():
    my_str = ":".join((TEST_LOGIN, TEST_PASSWORD)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/login', headers={"Authorization": "Basic " + credentials})
    return response

@pytest.fixture(scope="function")
def access_headers(token_response):
    access_token = token_response.json().get('access_token')
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    return headers

@pytest.fixture(scope="function")
def refresh_headers(token_response):
    refresh_token = token_response.json().get('refresh_token')
    headers = {
        'Authorization': 'Bearer ' + refresh_token
    }
    return headers

@pytest.fixture()
def not_access_headers(scope="function"):
    login = "not_user"
    password = "not_password"
    my_str = ":".join((login, password)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    access_token = credentials
    headers = {"Authorization": "Bearer " + access_token}
    return headers


def token_response_func(login, password):
    my_str = ":".join((login, password)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/login', headers={"Authorization": "Basic " + credentials})
    return response


def access_headers_func(login, password):
    access_token = token_response_func(login, password).json().get('access_token')
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    return headers

