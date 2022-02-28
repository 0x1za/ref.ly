import json


def test_index(test_client):
    assert test_client.get("/").status_code == 200


def test_create_referral_user_doesnt_exist(test_client, init_database):
    response = test_client.post(
        "/v1/create/referral",
        json={
            "invitee_email": "jackdoe@example.com",
            "referer_email": "jogn@example.com",
        },
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["data"] == {}
    assert data["errors"][0] == "User with email jogn@example.com does not exist."
    assert data["status"] == 0
