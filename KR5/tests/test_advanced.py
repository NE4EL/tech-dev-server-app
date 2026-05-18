"""Task 4: Dependency injection and advanced routing tests."""

TASK_DATA = {
    "title": "Advanced Task",
    "description": "Description",
    "status": "todo",
    "priority": 3,
}


def test_users_me(client):
    resp = client.get("/users/me", headers={"X-User-Id": "42"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 42


def test_users_me_no_auth(client):
    resp = client.get("/users/me")
    assert resp.status_code == 401


def test_admin_access_denied_for_regular_user(client):
    resp = client.get("/admin/stats", headers={"X-User-Id": "1"})
    assert resp.status_code == 403


def test_admin_stats(client, admin_headers):
    client.post("/tasks", json=TASK_DATA, headers=admin_headers)
    resp = client.get("/admin/stats", headers=admin_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "total_tasks" in data
    assert data["total_tasks"] >= 1
    assert "by_status" in data
    assert set(data["by_status"].keys()) == {"todo", "in_progress", "done"}


def test_delete_own_task(client, user_headers):
    create_resp = client.post("/tasks", json=TASK_DATA, headers=user_headers)
    task_id = create_resp.json()["id"]
    resp = client.delete(f"/tasks/{task_id}", headers=user_headers)
    assert resp.status_code == 204


def test_delete_others_task_returns_404(client):
    user1 = {"X-User-Id": "1"}
    user2 = {"X-User-Id": "2"}
    create_resp = client.post("/tasks", json=TASK_DATA, headers=user1)
    task_id = create_resp.json()["id"]
    resp = client.delete(f"/tasks/{task_id}", headers=user2)
    assert resp.status_code == 404


def test_admin_can_delete_any_task(client, admin_headers):
    user_headers = {"X-User-Id": "5"}
    create_resp = client.post("/tasks", json=TASK_DATA, headers=user_headers)
    task_id = create_resp.json()["id"]
    resp = client.delete(f"/admin/tasks/{task_id}", headers=admin_headers)
    assert resp.status_code == 204
