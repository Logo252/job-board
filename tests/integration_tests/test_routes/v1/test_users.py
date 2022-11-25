import json

from fastapi import status


def test_create_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "testing_password",
    }
    response = client.post("/v1/users/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@gmail.com"
    assert response.json()["is_active"] == True


def test_get_user_successful_response(client):
    data = {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "testing_password",
    }
    response = client.post("/v1/users/", json.dumps(data))
    response = response.json()
    id = response["id"]

    response = client.get("/v1/users/{0}".format(id))
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["username"] == "testuser"
    assert json_response["email"] == "testuser@gmail.com"


def test_get_user_not_found_response(client):
    _id = 999999

    response = client.get("/v1/users/{0}".format(_id))
    assert response.status_code == 404


def test_patch_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "testing_password",
    }
    response = client.post("/v1/users/", json.dumps(data))
    response = response.json()
    id = response["id"]

    data["username"] = "test new username"
    response = client.patch("/v1/users/{0}".format(id), json.dumps(data))
    json_response = response.json()

    assert response.status_code == 200


def test_patch_user_not_found_response(client):
    _id = 999999

    response = client.patch("/v1/users/{0}".format(_id), json.dumps({}))

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "testing_password",
    }
    response = client.post("/v1/users/", json.dumps(data))
    response = response.json()
    id = response["id"]

    response = client.delete("/v1/users/{0}".format(id))

    assert response.status_code == status.HTTP_200_OK


def test_delete_user_not_found_response(client):
    _id = 999999

    response = client.get("/v1/users/{0}".format(_id))

    assert response.status_code == status.HTTP_404_NOT_FOUND
