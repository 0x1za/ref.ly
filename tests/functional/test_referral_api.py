import json


def test_index(test_client):
    assert test_client.get("/").status_code == 200


def test_get_all_referrals(test_client, init_database):
    response = test_client.get("/v1/referrals")
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["errors"] == []
    assert data["status"] == 1
    assert data["message"] == "Query results: 1 records"


def test_get_one_referral_with_id(test_client, init_database):
    response = test_client.get("/v1/referrals?id=1")
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["errors"] == []
    assert data["status"] == 1
    assert data["message"] == "Query results: 1 records"


def test_get_one_referral_with_referral_code(test_client, init_database):
    response = test_client.get("/v1/referrals?referral_code=0WXOGQI")
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["errors"] == []
    assert data["status"] == 1
    assert data["message"] == "Query results: 1 records"


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


def test_create_referral_invalid_invitee(test_client, init_database):
    response = test_client.post(
        "/v1/create/referral",
        json={
            "invitee_email": "invalid.com",
            "referer_email": "johndoe@example.com",
        },
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["errors"][0] == "invitee_email: invalid.com is not a valid email."
    assert data["status"] == 0


def test_create_referral_invalid_email_referer(test_client, init_database):
    response = test_client.post(
        "/v1/create/referral",
        json={
            "invitee_email": "joe@valid.com",
            "referer_email": "johndoe-invalid.com",
        },
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert (
        data["errors"][0] == "referer_email: johndoe-invalid.com is not a valid email."
    )
    assert data["status"] == 0


def test_create_referral_user_already_exists(test_client, init_database):
    response = test_client.post(
        "/v1/create/referral",
        json={
            "invitee_email": "janedoe@example.com",
            "referer_email": "johndoe@example.com",
        },
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["errors"][0] == "User with email johndoe@example.com already exists."
    assert data["status"] == 0


def test_create_referral_user_invalid_payload_invitee(test_client, init_database):
    response = test_client.post(
        "/v1/create/referral",
        json={
            "x": "janedoe@example.com",
            "referer_email": "johndoe@example.com",
        },
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["errors"][0] == "A required key 'invitee_email' was not provided."
    assert data["status"] == 0


def test_create_referral_user_invalid_payload_referer(test_client, init_database):
    response = test_client.post(
        "/v1/create/referral",
        json={
            "invitee_email": "janedoe@example.com",
            "y": "johndoe@example.com",
        },
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["errors"][0] == "A required key 'referer_email' was not provided."
    assert data["status"] == 0
