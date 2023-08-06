from lnhub_rest.main import client
from lnhub_rest.routers.account import (
    get_account_by_handle,
    get_account_by_id,
    get_account_instances,
)

account_expected = {
    "id": "2e35fa63-05d6-47f6-9d40-c56383ff04a3",
    "lnid": "j5ea1UV7",
    "handle": "static-testuser1",
    "name": None,
    "bio": None,
    "website": None,
    "github_handle": None,
    "twitter_handle": None,
    "linkedin_handle": None,
    "created_at": "2023-02-10T15:55:03.340037",
    "updated_at": None,
    "user_id": "2e35fa63-05d6-47f6-9d40-c56383ff04a3",
    "avatar_url": None,
}


def test_get_account_by_id():
    account = get_account_by_id("2e35fa63-05d6-47f6-9d40-c56383ff04a3")
    assert str(account) == str(account_expected)


def test_get_account_by_id_rest():
    response = client.get("/account/2e35fa63-05d6-47f6-9d40-c56383ff04a3")
    assert str(response.json()) == str(account_expected)


def test_get_account_by_handle():
    account = get_account_by_handle("static-testuser1")
    assert str(account) == str(account_expected)


def test_get_account_by_handle_rest():
    response = client.get("/account/handle/static-testuser1")
    assert str(response.json()) == str(account_expected)


account_instances_expected = [
    {
        "id": "511131e1-71dd-42ab-a37a-5a914d7efc3d",
        "account_id": "2e35fa63-05d6-47f6-9d40-c56383ff04a3",
        "name": "static-testinstance1",
        "storage_id": "a57cf777-a606-4c72-813e-443163b6c244",
        "db": None,
        "schema_str": "",
        "created_at": "2023-02-10T16:22:25.462808",
        "updated_at": None,
        "description": None,
        "public": False,
        "account": {
            "handle": "static-testuser1",
            "id": "2e35fa63-05d6-47f6-9d40-c56383ff04a3",
        },
    }
]


def test_get_account_instances():
    instances = get_account_instances("static-testuser1")
    assert str(instances) == str(account_instances_expected)


def test_get_account_instances_rest():
    response = client.get("/account/resources/owned/instances/static-testuser1")
    assert str(response.json()) == str(account_instances_expected)
