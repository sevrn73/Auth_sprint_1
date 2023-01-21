import os
import requests
from http import HTTPStatus
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()


def test_sign_up(user):
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/login',
        auth=HTTPBasicAuth('test_login', 'test_password'),
    )
    assert response.status_code == HTTPStatus.OK
