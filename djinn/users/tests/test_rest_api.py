import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_login(api_client, bucky):
    url = "/api/login/"
    print(bucky.email, "username")
    data = {"email": bucky.email, "password": "pass1234"}
    response = APIClient().post(url, data, format="json")
    assert response.status_code == 200

    expected_keys = ["authentication", "user"]
    assert all(key in response.data for key in expected_keys)

    expected_authentication_keys = ["access_token", "refresh_token"]
    assert all(
        key in response.data["authentication"] for key in expected_authentication_keys
    )
    # assert response.data["user"] == {
    #     "avatar": None,
    #     "id": bucky.id,
    #     "username": bucky.username,
    # }
