import os
import pytest
import requests
from dotenv import load_dotenv
load_dotenv()


@pytest.fixture()
def user():
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/sign_up',
        data={'login': 'test_login', 'password': 'test_password'},
    )

    return response.json
