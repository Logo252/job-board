import json


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

# Add tests for new routes here
