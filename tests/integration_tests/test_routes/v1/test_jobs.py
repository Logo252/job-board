import json

from fastapi import status


def test_create_job(client):
    data = {
        "title": "Statybininko",
        "company": "test",
        "company_url": "www.statybos.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-11-05",
    }
    response = client.post("/v1/jobs/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["company"] == "test"
    assert response.json()["description"] == "python"


def test_get_job_successful_response(client):
    data = {
        "title": "Teacher",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-03-20",
    }
    response = client.post("v1/jobs/", json.dumps(data))
    response = response.json()
    id = response["id"]

    response = client.get("v1/jobs/{0}".format(id))
    assert response.status_code == 200
    assert response.json()["title"] == "Teacher"


def test_get_job_not_found_response(client):
    _id = 999999

    response = client.get("v1/jobs/{0}".format(_id))
    assert response.status_code == 404


def test_read_all_active_jobs(client):
    data = {
        "title": "Teacher",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-03-20",
    }
    client.post("/v1/jobs", json.dumps(data))
    client.post("/v1/jobs", json.dumps(data))

    response = client.get("/v1/jobs")
    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]


def test_update_a_job(client):
    data = {
        "title": "New Job title",
        "company": "test company",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "test",
        "date_posted": "2022-03-20",
    }
    client.post("/v1/jobs", json.dumps(data))
    data["title"] = "test new title"
    response = client.put("/v1/jobs/1", json.dumps(data))
    assert response.status_code == 200


def test_delete_a_job(client):
    data = {
        "title": "New Job title",
        "company": "test company",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "test",
        "date_posted": "2022-03-20",
    }
    client.post("/v1/jobs", json.dumps(data))
    client.delete("/v1/jobs/1")
    response = client.get("/v1/jobs/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
