from typing import Dict
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string
import urllib3
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.item import create_random_item


def test_create_delete_bekpacktrip(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    # create the user
    user = create_random_user(db)
    data = {"owner_id": user.id}
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpackusers/",
        headers=normal_user_token_headers,
        json=data,
    )
    content = response.json()
    assert "id" in content
    assert "owner_id" in content
    assert "is_active" in content
    assert content["is_active"] == True
    user_id_old = content["id"]
    # create trip
    trip_data = {"name": random_lower_string(), "color": "black"}
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=normal_user_token_headers,
        json=trip_data,
    )
    content = response.json()
    trip_id = content["id"]
    assert "id" in content
    for k, v in trip_data.items():
        assert content[k] == v
    # delete trip
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{trip_id}",
        headers=normal_user_token_headers,
    )
    # then delete user
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpackusers/{user_id_old}",
        headers=normal_user_token_headers,
    )
    content_new = response.json()
    assert "id" in content_new
    assert content_new["id"] == user_id_old
