from typing import Dict
from app.tests.utils.user import authentication_token_from_email, create_random_user
import urllib3
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.item import create_random_item
from app import crud


def test_create_delete_bekpackuser(client: TestClient, db: Session) -> None:
    # create the user
    user = create_random_user(db)
    headers = authentication_token_from_email(client=client, email=user.email, db=db)
    # enable BekPack for the user
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpackusers/",
        headers=headers,
        json={},
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "owner_id" in content
    assert "is_active" in content
    assert content["is_active"] == True
    id_old = content["id"]
    assert crud.bekpackuser.get(db=db, id=id_old, user=user)
    # then delete it
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpackusers/me/profile",
        headers=headers,
    )
    assert (
        response.status_code == 200
    ), f"delete failed {user.id} {id_old} {response.status_code} {response.content}"

    content_new = response.json()
    assert "id" in content_new
    assert content_new["id"] == id_old
