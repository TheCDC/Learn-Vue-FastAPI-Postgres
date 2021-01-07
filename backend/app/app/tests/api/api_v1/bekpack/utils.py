from app.core.config import settings
from app.tests.utils.user import create_random_user
from sqlalchemy.orm.session import Session
from starlette.testclient import TestClient


def get_bekpack_user(client: TestClient, normal_user_token_headers_random, db: Session):
    user = create_random_user(db)
    data = {"owner_id": user.id}
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpackusers/",
        headers=normal_user_token_headers_random,
        json=data,
    )
    return response
