import json


def test_index(test_client):
    assert test_client.get("/").status_code == 200


def test_create_users_valid(test_client, init_database):
    response = test_client.post(
        "/v1/create/user", json={"username": "fibby", "email": "Fibby@example.com"}
    )
    data = json.loads(response.get_data(as_text=True))
    print(data)
    assert response.status_code == 200
    assert data["data"]["current_balance"] == "0"
    assert data["data"]["email"] == "Fibby@example.com"
    assert data["data"]["username"] == "fibby"
    assert data["status"] == 1


def test_create_users_email_not_provided(test_client):
    response = test_client.post("/v1/create/user", json={"username": "JohnDoe"})
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["status"] == 0
    assert data["errors"][0] == "A required key 'email' was not provided."


def test_create_users_username_not_provided(test_client):
    response = test_client.post(
        "/v1/create/user", json={"username": "johndoe", "email": "johndoes@example.com"}
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["status"] == 0
    assert data["errors"][0] == "UNIQUE constraint failed: user.username"


def test_create_user_email_already_exists(test_client):
    response = test_client.post(
        "/v1/create/user", json={"username": "Fibby", "email": "johndoe@example.com"}
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["status"] == 0
    assert data["errors"][0] == "UNIQUE constraint failed: user.email"
