from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.crud.crud_bekpack.crud_bekpacktrip import bekpacktrip
from app.schemas.bekpack.bekpacktrip import BekpackTrip, BekpackTripCreate
from app.tests.api.api_v1.bekpack.utils import create_bekpack_user
from app.tests.crud.bekpack.utils import get_random_color
from app.tests.utils.bekpack import create_random_trip
from app.tests.utils.user import authentication_token_from_email, create_random_user
from app.tests.utils.utils import random_lower_name, random_lower_string


def test_create_bekpacktrip(client: TestClient, db: Session) -> None:
    # create the user
    bp_user = create_bekpack_user(db=db)
    auth_token = authentication_token_from_email(
        db=db, client=client, email=bp_user.owner.email
    )
    # create trip
    trip_data = {
        "name": random_lower_name(),
        "color": get_random_color(),
        "description": random_lower_string(),
    }
    trip = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=auth_token,
        json=trip_data,
    )
    content = trip.json()
    assert "id" in content, "post failed"
    trip_id = content["id"]
    assert BekpackTrip(**content)
    assert "id" in content
    for key, value in trip_data.items():
        assert content[key] == value
    # get trip

    trip = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{trip_id}",
        headers=auth_token,
    )
    assert trip.status_code == 200, f"{trip.content}"
    content = trip.json()
    assert "id" in content, f"get failed {content}"
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
    assert [BekpackTrip(**i) for i in content]
    assert len(content) == len(trips)
    assert set(t["id"] for t in content) == set(t.id for t in trips)


def test_get_bekpacktrip_select_by_string(client: TestClient, db: Session) -> None:
    owner = create_random_user(db=db)
    bp_user = create_bekpack_user(db=db, owner=owner)
    token = authentication_token_from_email(db=db, client=client, email=owner.email)
    trip = bekpacktrip.create_with_owner(
        db=db,
        obj_in=BekpackTripCreate(
            name=random_lower_name(),
            color=get_random_color(),
            description=random_lower_string(),
        ),
        owner=owner,
    )
    response = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/select/by_string?filter_string={trip.name}",
        headers=token,
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


def test_get_bekpacktrip_mine_multi(client: TestClient, db: Session) -> None:
    owner = create_random_user(db=db)
    token_headers = authentication_token_from_email(
        client=client, email=owner.email, db=db
    )
    # create the user
    bp_user = create_bekpack_user(owner=owner, db=db)
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
        bekpacktrip.create_with_owner(db=db, obj_in=t, owner=owner)
    # get trip

    response = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/mine/all",
        headers=token_headers,
    )
    content = response.json()
    assert "items" in content
    trips = [BekpackTrip(**i) for i in content["items"]]
    assert trips

    got_ids = set(t.id for t in trips)
    target_ids = set([i.id for i in bekpacktrip.get_by_owner(db=db, owner_id=owner.id)])
    assert got_ids == target_ids


def test_get_bekpacktrip_invalid(
    client: TestClient, normal_user_token_headers_random: Dict[str, str], db: Session
) -> None:
    # get trip

    response = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/-1",
        headers=normal_user_token_headers_random,
    )
    assert response.status_code == 404


def test_get_bekpacktrip_unauthorized(
    client: TestClient,
    db: Session,
) -> None:
    # register both users for bekpack
    user = create_bekpack_user(db=db)
    normal_user_token_headers_random = authentication_token_from_email(
        client=client, email=user.owner.email, db=db
    )
    trip = create_random_trip(db=db)
    # get trip as random user
    response = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{trip.id}",
        headers=normal_user_token_headers_random,
    )
    assert response.status_code == 404, f"{response.content}"


def test_get_bekpacktrip_all_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:

    # get trips

    response = client.get(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=superuser_token_headers,
    )
    content = response.json()
    target_num = len(bekpacktrip.get_all(db=db))
    assert "items" in content
    assert [BekpackTrip(**i) for i in content["items"]]

    assert "page" in content
    assert "total" in content
    assert content["total"] == target_num


def test_delete_bekpacktrip(client: TestClient, db: Session) -> None:

    # create the user
    bp_user = create_bekpack_user(db=db)
    auth_token = authentication_token_from_email(
        db=db, client=client, email=bp_user.owner.email
    )
    # create trip
    trip_data = {
        "name": random_lower_name(),
        "color": get_random_color(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=auth_token,
        json=trip_data,
    )
    content = response.json()
    trip_id = content["id"]
    assert "id" in content
    assert BekpackTrip(**content)
    for key, value in trip_data.items():
        assert content[key] == value
    # delete trip
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{trip_id}",
        headers=auth_token,
    )
    content = response.json()
    assert "id" in content

    assert content["id"] == trip_id


def test_update_bekpacktrip(
    client: TestClient, normal_user_token_headers_random: Dict[str, str], db: Session
) -> None:

    trip = create_random_trip(db=db)
    token = authentication_token_from_email(
        client=client, db=db, email=trip.owner.owner.email
    )
    # update trip
    content_update = {"color": get_random_color(), "name": random_lower_name()}
    response = client.put(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{trip.id}",
        headers=token,
        json=content_update,
    )
    assert response.status_code == 200
    content = response.json()
    assert BekpackTrip(**content)

    # assertions
    for k, v in content_update.items():
        assert content[k] == v


def test_update_bekpacktrip_nonexistent(
    client: TestClient, normal_user_token_headers_random: Dict[str, str], db: Session
) -> None:

    # create the user
    response = create_bekpack_user(db=db)
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
    response = create_bekpack_user(db=db)
    # update trip
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/-1",
        headers=normal_user_token_headers_random,
    )
    assert response.status_code == 200


def test_delete_bekpacktrip_unauthorized(
    client: TestClient,
    db: Session,
) -> None:
    # register both users for bekpack
    user_first = create_bekpack_user(db=db)
    user_second = create_bekpack_user(db=db)

    # create trip as nonrandom user
    trip_data = {
        "name": random_lower_name(),
        "color": get_random_color(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=authentication_token_from_email(
            client=client, email=user_first.owner.email, db=db
        ),
        json=trip_data,
    )
    assert response.status_code == 200, f"{response.content}"
    content = response.json()
    created_trip_id = content["id"]

    # update trip as random user
    response = client.delete(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{created_trip_id}",
        headers=authentication_token_from_email(
            client=client, email=user_second.owner.email, db=db
        ),
    )
    assert response.status_code == 404, f"{response.content}"


def test_update_bekpacktrip_unauthorized(
    client: TestClient,
    db: Session,
) -> None:
    # register both users for bekpack
    user1 = create_bekpack_user(db=db)
    user2 = create_bekpack_user(db=db)

    # create trip as nonrandom user
    trip_data = {
        "name": random_lower_name(),
        "color": get_random_color(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/",
        headers=authentication_token_from_email(
            client=client, db=db, email=user1.owner.email
        ),
        json=trip_data,
    )
    print(response.content)
    assert response.status_code == 200, f"{response.content}"
    content = response.json()
    created_trip_id = content["id"]

    # update trip as random user
    response = client.put(
        f"{settings.API_V1_STR}/bekpack/bekpacktrips/{created_trip_id}",
        headers=authentication_token_from_email(
            client=client, db=db, email=user2.owner.email
        ),
        json={
            "name": random_lower_name(),
            "color": get_random_color(),
            "description": random_lower_string(),
        },
    )
    assert response.status_code == 404, f"{response.content}"
