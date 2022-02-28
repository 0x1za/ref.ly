import json


def test_index(test_client):
    assert test_client.get("/").status_code == 200


def test_create_users_valid(test_client, init_database):
    response = test_client.post(
        "/v1/create/user", json={"username": "x123", "email": "x123@example.com"}
    )
    data = json.loads(response.get_data(as_text=True))
    print(data)
    assert response.status_code == 200
    assert data["data"]["current_balance"] == "0"
    assert data["data"]["email"] == "x123@example.com"
    assert data["data"]["username"] == "x123"
    assert data["status"] == 1


def test_create_users_email_not_provided(test_client):
    response = test_client.post("/v1/create/user", json={"username": "x234"})
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["status"] == 0
    assert data["errors"][0] == "A required key 'email' was not provided."


def test_create_user_username_not_provided(test_client):
    response = test_client.post("/v1/create/user", json={"email": "x234@example.com"})
    data = json.loads(response.get_data(as_text=True))
    print(data)
    assert response.status_code == 200
    assert data["status"] == 0
    assert data["errors"][0] == "A required key 'username' was not provided."


def test_create_user_email_already_exists(test_client, init_database):
    response = test_client.post(
        "/v1/create/user", json={"username": "x234", "email": "johndoe@example.com"}
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["status"] == 0
    assert data["errors"][0] == "UNIQUE constraint failed: user.email"


def test_create_user_username_already_exists(test_client, init_database):
    response = test_client.post(
        "/v1/create/user", json={"username": "johndoe", "email": "x234@example.com"}
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["status"] == 0
    assert data["errors"][0] == "UNIQUE constraint failed: user.username"


def test_create_user_with_referral_code(test_client, init_database):
    response = test_client.post(
        "/v1/create/user",
        json={
            "username": "johndoe",
            "email": "x234@example.com",
            "referral_code": "0WXOGQI",
        },
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["status"] == 0
    assert data["errors"][0] == "UNIQUE constraint failed: user.username"
