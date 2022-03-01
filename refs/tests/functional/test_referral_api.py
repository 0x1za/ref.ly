import json


def test_index(test_client):
    assert test_client.get("/").status_code == 200


def test_create_referral_user_doesnt_exist(test_client, init_database):
    response = test_client.post(
        "/v1/create/referral",
        json={
            "invitee_email": "jackdoe@example.com",
            "referer_email": "x234@example.com",
        },
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["data"] == {}
    assert data["errors"][0] == "User with email x234@example.com does not exist."
    assert data["status"] == 0


def test_referral_record_already_exist(test_client, init_database):
    response = test_client.post(
        "/v1/create/referral",
        json={
            "invitee_email": "invited_user@example.com",
            "referer_email": "johndoe@example.com",
        },
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["data"] == {}
    assert (
        data["errors"][0]
        == "You have already invited user with email `invited_user@example.com`"
    )
    assert data["status"] == 0


def test_create_referral_valid(test_client, init_database):
    response = test_client.post(
        "/v1/create/referral",
        json={
            "invitee_email": "invited_user_2@example.com",
            "referer_email": "johndoe@example.com",
        },
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["message"] == "Referral successfully created"
    assert data["status"] == 1


def test_create_referral_to_self(test_client, init_database):
    response = test_client.post(
        "/v1/create/referral",
        json={
            "invitee_email": "johndoe@example.com",
            "referer_email": "johndoe@example.com",
        },
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["errors"][0] == "You cannot send a referral to yourself."
    assert data["status"] == 0
