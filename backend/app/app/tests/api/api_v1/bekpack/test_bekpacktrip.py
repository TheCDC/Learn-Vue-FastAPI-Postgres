from typing import Dict
from app.tests.api.api_v1.bekpack.utils import get_bekpack_user
from app.tests.crud.bekpack.utils import get_random_color
from app.tests.utils.utils import random_lower_string
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test_create_delete_bekpacktrip(
    client: TestClient, normal_user_token_headers_random: Dict[str, str], db: Session
) -> None:

    # create the user
    response = get_bekpack_user(client, normal_user_token_headers_random, db)
    content = response.json()
    assert "id" in content
    assert "owner_id" in content
    assert "is_active" in content
    assert content["is_active"] == True
    user_id_old = content["id"]
    # create trip
    trip_data = {"name": random_lower_string(), "color": get_random_color()}
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=normal_user_token_headers_random,
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
        headers=normal_user_token_headers_random,
    )
    # then delete user
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpackusers/{user_id_old}",
        headers=normal_user_token_headers_random,
    )
    content_new = response.json()
    assert "id" in content_new
    assert content_new["id"] == user_id_old


def test_update_bekpacktrip(
    client: TestClient, normal_user_token_headers_random: Dict[str, str], db: Session
) -> None:

    # create the user
    response = get_bekpack_user(client, normal_user_token_headers_random, db)
    content = response.json()
    user_id_old = content["id"]
    # create trip
    trip_data = {"name": random_lower_string(), "color": get_random_color()}
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=normal_user_token_headers_random,
        json=trip_data,
    )
    content = response.json()
    trip_id_created = content["id"]
    # update trip
    content_update = {"color": get_random_color(), "name": "newname"}
    response = client.put(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{trip_id_created}",
        headers=normal_user_token_headers_random,
        json=content_update,
    )
    content = response.json()
    for k, v in content_update.items():
        assert content[k] == v
    # delete trip
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{trip_id_created}",
        headers=normal_user_token_headers_random,
    )
    # then delete user
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpackusers/{user_id_old}",
        headers=normal_user_token_headers_random,
    )
    content_new = response.json()
    assert "id" in content_new
    assert content_new["id"] == user_id_old
