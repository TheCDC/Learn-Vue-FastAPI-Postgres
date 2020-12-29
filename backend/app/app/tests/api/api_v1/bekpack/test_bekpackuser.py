from typing import Dict
from app.tests.utils.user import create_random_user
import urllib3
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.item import create_random_item


def test_create_delete_bekpackuser(
    client: TestClient, normal_user_token_headers_random: Dict[str, str], db: Session
) -> None:
    # create the user
    user = create_random_user(db)
    data = {"owner_id": user.id}
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpackusers/",
        headers=normal_user_token_headers_random,
        json=data,
    )
    content = response.json()
    assert "id" in content
    assert "owner_id" in content
    assert "is_active" in content
    assert content["is_active"] == True
    id_old = content["id"]
    # then delete it
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpackusers/{id_old}",
        headers=normal_user_token_headers_random,
    )
    content_new = response.json()
    assert "id" in content_new
    assert content_new["id"] == id_old
