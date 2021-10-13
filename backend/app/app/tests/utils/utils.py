import random
import string
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from app.core.config import settings
from app import models


def random_lower_string(length=32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_lower_name(words=3) -> str:
    return " ".join(
        random_lower_string(length=random.randint(3, 8)) for _ in range(words)
    )


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    try:

        a_token = tokens["access_token"]
    except KeyError as e:
        print(tokens, login_data)
        raise e
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
