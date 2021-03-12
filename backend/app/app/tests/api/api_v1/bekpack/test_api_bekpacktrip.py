from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.crud_bekpack.crud_bekpacktrip import bekpacktrip
from app.schemas.bekpack.bekpacktrip import BekpackTrip, BekpackTripCreate
from app.tests.api.api_v1.bekpack.utils import get_bekpack_user
from app.tests.crud.bekpack.utils import get_random_color
from app.tests.utils.utils import random_lower_name, random_lower_string
from app import schemas, crud


def test_create_bekpacktrip(
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
    trip_data = {
        "name": random_lower_name(),
        "color": get_random_color(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=normal_user_token_headers_random,
        json=trip_data,
    )
    content = response.json()
    trip_id = content["id"]
    assert "id" in content
    for key, value in trip_data.items():
        assert content[key] == value
    # get trip

    response = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{trip_id}",
        headers=normal_user_token_headers_random,
    )
    content = response.json()
    assert "id" in content
    assert content["id"] == trip_id


def test_get_bekpacktrip_select_by_ids_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    trips = [
        bekpacktrip.create(
            db=db,
            obj_in=BekpackTripCreate(
                name=random_lower_name(),
                color=get_random_color(),
                description=random_lower_string(),
            ),
        )
        for _ in range(5)
    ]

    query_params_string = "".join(["&ids=" + str(t.id) for t in trips])
    response = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/select/by_ids?{query_params_string}",
        headers=superuser_token_headers,
    )
    print(response.content)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == len(trips)
    assert set(t["id"] for t in content) == set(t.id for t in trips)


def test_get_bekpacktrip_select_by_string_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    trip = bekpacktrip.create(
        db=db,
        obj_in=BekpackTripCreate(
            name=random_lower_name(),
            color=get_random_color(),
            description=random_lower_string(),
        ),
    )
    response = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/select/by_string?filter_string={trip.name}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    print(content)

    found_records = [
        schemas.BekpackTrip(**i) for i in content["items"] if i["id"] == trip.id
    ]
    assert len(found_records) > 0
    found = found_records[0]
    assert found
    assert found.name == trip.name
    assert found.description == trip.description


def test_delete_bekpacktrip_multi_by_ids(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    trips = [
        bekpacktrip.create(
            db=db,
            obj_in=BekpackTripCreate(
                name=random_lower_name(),
                color=get_random_color(),
                description=random_lower_string(),
            ),
        )
        for _ in range(5)
    ]
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=superuser_token_headers,
        json=[t.id for t in trips],
    )
    assert response.status_code == 200
    content = response.json()
    assert content == len(trips)


def test_get_bekpacktrip_mine_multi(
    client: TestClient, normal_user_token_headers_random: Dict[str, str], db: Session
) -> None:
    # create the user
    response = get_bekpack_user(client, normal_user_token_headers_random, db)
    user = response.json()
    # create trip
    trips = [
        BekpackTripCreate(
            name=random_lower_name(),
            color=get_random_color(),
            description=random_lower_string(),
        )
        for _ in range(5)
    ]
    for t in trips:
        bekpacktrip.create(db=db, obj_in=t)
    # get trip

    response = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/mine/all",
        headers=normal_user_token_headers_random,
    )
    content = response.json()
    assert "items" in content
    got_ids = set(i.id for i in content["items"])
    target_ids = set(
        [i.id for i in bekpacktrip.get_by_owner(db=db, owner_id=user["id"])]
    )
    assert got_ids == target_ids


def test_get_bekpacktrip_invalid(
    client: TestClient, normal_user_token_headers_random: Dict[str, str], db: Session
) -> None:
    # create the user
    response = get_bekpack_user(client, normal_user_token_headers_random, db)
    user = response.json()
    # get trip

    response = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/-1",
        headers=normal_user_token_headers_random,
    )
    assert response.status_code == 404


def test_get_bekpacktrip_unauthorized(
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
    normal_user_token_headers_random: Dict[str, str],
    db: Session,
) -> None:
    # register both users for bekpack
    response_first_user = get_bekpack_user(client, normal_user_token_headers_random, db)
    response = get_bekpack_user(client, normal_user_token_headers, db)
    user = response.json()

    # create trip as nonrandom user
    trip_data = {
        "name": random_lower_name(),
        "color": get_random_color(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=normal_user_token_headers,
        json=trip_data,
    )
    print(response.content)
    assert response.status_code == 200
    content = response.json()
    created_trip_id = content["id"]

    # get trip as random user
    response = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{created_trip_id}",
        headers=normal_user_token_headers_random,
    )
    assert response.status_code == 403


def test_get_bekpacktrip_all_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    # create the user
    response = get_bekpack_user(client, superuser_token_headers, db)
    user = response.json()

    # get trips

    response = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/", headers=superuser_token_headers,
    )
    content = response.json()
    target_num = len(bekpacktrip.get_all(db=db))
    assert "items" in content
    assert "page" in content
    assert "total" in content
    assert content["total"] == target_num


def test_delete_bekpacktrip(
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
    trip_data = {
        "name": random_lower_name(),
        "color": get_random_color(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=normal_user_token_headers_random,
        json=trip_data,
    )
    content = response.json()
    trip_id = content["id"]
    assert "id" in content
    for key, value in trip_data.items():
        assert content[key] == value
    # delete trip
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{trip_id}",
        headers=normal_user_token_headers_random,
    )
    content = response.json()
    assert "id" in content

    assert content["id"] == trip_id


def test_update_bekpacktrip(
    client: TestClient, normal_user_token_headers_random: Dict[str, str], db: Session
) -> None:

    # create the user
    response = get_bekpack_user(client, normal_user_token_headers_random, db)
    content = response.json()
    user_id_old = content["id"]
    # create trip
    trip_data = {"name": random_lower_name(), "color": get_random_color()}
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=normal_user_token_headers_random,
        json=trip_data,
    )
    content = response.json()
    trip_id_created = content["id"]
    # update trip
    content_update = {"color": get_random_color(), "name": random_lower_name()}
    response = client.put(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{trip_id_created}",
        headers=normal_user_token_headers_random,
        json=content_update,
    )
    content = response.json()
    # assertions
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


def test_update_bekpacktrip_nonexistent(
    client: TestClient, normal_user_token_headers_random: Dict[str, str], db: Session
) -> None:

    # create the user
    response = get_bekpack_user(client, normal_user_token_headers_random, db)
    # update trip
    content_update = {"color": get_random_color(), "name": random_lower_name()}
    response = client.put(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/-1",
        headers=normal_user_token_headers_random,
        json=content_update,
    )
    assert response.status_code == 404


def test_delete_bekpacktrip_nonexistent(
    client: TestClient, normal_user_token_headers_random: Dict[str, str], db: Session
) -> None:

    # create the user
    response = get_bekpack_user(client, normal_user_token_headers_random, db)
    # update trip
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/-1",
        headers=normal_user_token_headers_random,
    )
    assert response.status_code == 404


def test_delete_bekpacktrip_unauthorized(
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
    normal_user_token_headers_random: Dict[str, str],
    db: Session,
) -> None:
    # register both users for bekpack
    response = get_bekpack_user(client, normal_user_token_headers_random, db)
    response = get_bekpack_user(client, normal_user_token_headers, db)
    user = response.json()

    # create trip as nonrandom user
    trip_data = {
        "name": random_lower_name(),
        "color": get_random_color(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=normal_user_token_headers,
        json=trip_data,
    )
    print(response.content)
    assert response.status_code == 200
    content = response.json()
    created_trip_id = content["id"]

    # update trip as random user
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{created_trip_id}",
        headers=normal_user_token_headers_random,
    )
    assert response.status_code == 403


def test_update_bekpacktrip_unauthorized(
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
    normal_user_token_headers_random: Dict[str, str],
    db: Session,
) -> None:
    # register both users for bekpack
    response = get_bekpack_user(client, normal_user_token_headers_random, db)
    response = get_bekpack_user(client, normal_user_token_headers, db)
    user = response.json()

    # create trip as nonrandom user
    trip_data = {
        "name": random_lower_name(),
        "color": get_random_color(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=normal_user_token_headers,
        json=trip_data,
    )
    print(response.content)
    assert response.status_code == 200
    content = response.json()
    created_trip_id = content["id"]

    # update trip as random user
    response = client.put(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{created_trip_id}",
        headers=normal_user_token_headers_random,
        json={
            "name": random_lower_name(),
            "color": get_random_color(),
            "description": random_lower_string(),
        },
    )
    assert response.status_code == 403
