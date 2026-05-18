"""Task 1: Integration tests for Task Management API."""

TASK_DATA = {
    "title": "My Task",
    "description": "Task description",
    "status": "todo",
    "priority": 3,
}


def test_create_task(client, user_headers):
    resp = client.post("/tasks", json=TASK_DATA, headers=user_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "My Task"
    assert data["owner_id"] == 10
    assert data["status"] == "todo"


def test_create_task_title_too_short(client, user_headers):
    resp = client.post("/tasks", json={**TASK_DATA, "title": "ab"}, headers=user_headers)
    assert resp.status_code == 422


def test_create_task_no_auth(client):
    resp = client.post("/tasks", json=TASK_DATA)
    assert resp.status_code == 401


def test_data_isolation(client):
    user1 = {"X-User-Id": "1"}
    user2 = {"X-User-Id": "2"}
    client.post("/tasks", json=TASK_DATA, headers=user1)
    resp = client.get("/tasks", headers=user2)
    assert resp.status_code == 200
    assert resp.json() == []


def test_filter_by_status(client, user_headers):
    client.post("/tasks", json={**TASK_DATA, "status": "todo"}, headers=user_headers)
    client.post("/tasks", json={**TASK_DATA, "status": "done"}, headers=user_headers)
    resp = client.get("/tasks?status=done", headers=user_headers)
    assert resp.status_code == 200
    tasks = resp.json()
    assert len(tasks) == 1
    assert tasks[0]["status"] == "done"


def test_filter_by_min_priority(client, user_headers):
    client.post("/tasks", json={**TASK_DATA, "priority": 2}, headers=user_headers)
    client.post("/tasks", json={**TASK_DATA, "priority": 4}, headers=user_headers)
    resp = client.get("/tasks?min_priority=3", headers=user_headers)
    assert resp.status_code == 200
    tasks = resp.json()
    assert len(tasks) == 1
    assert tasks[0]["priority"] == 4


def test_update_status(client, user_headers):
    create_resp = client.post("/tasks", json=TASK_DATA, headers=user_headers)
    task_id = create_resp.json()["id"]
    resp = client.patch(
        f"/tasks/{task_id}/status",
        json={"status": "done"},
        headers=user_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "done"


def test_unauthorized_task_access(client):
    user1 = {"X-User-Id": "1"}
    user2 = {"X-User-Id": "2"}
    create_resp = client.post("/tasks", json=TASK_DATA, headers=user1)
    task_id = create_resp.json()["id"]
    resp = client.get(f"/tasks/{task_id}", headers=user2)
    assert resp.status_code == 404


def test_delete_task(client, user_headers):
    create_resp = client.post("/tasks", json=TASK_DATA, headers=user_headers)
    task_id = create_resp.json()["id"]
    resp = client.delete(f"/tasks/{task_id}", headers=user_headers)
    assert resp.status_code == 204
    resp = client.get(f"/tasks/{task_id}", headers=user_headers)
    assert resp.status_code == 404
