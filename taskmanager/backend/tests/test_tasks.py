from fastapi import status


def test_create_task(client, auth_headers):
    res = client.post("/tasks", json={"title": "Buy milk", "description": "Whole milk"}, headers=auth_headers)
    assert res.status_code == status.HTTP_201_CREATED
    data = res.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False


def test_create_task_unauthenticated(client):
    res = client.post("/tasks", json={"title": "No auth"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_tasks(client, auth_headers):
    client.post("/tasks", json={"title": "Task 1"}, headers=auth_headers)
    client.post("/tasks", json={"title": "Task 2"}, headers=auth_headers)
    res = client.get("/tasks", headers=auth_headers)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["total"] == 2
    assert len(data["tasks"]) == 2


def test_list_tasks_filter_completed(client, auth_headers):
    r = client.post("/tasks", json={"title": "Task A"}, headers=auth_headers)
    task_id = r.json()["id"]
    client.post("/tasks", json={"title": "Task B"}, headers=auth_headers)
    client.put(f"/tasks/{task_id}", json={"completed": True}, headers=auth_headers)

    res = client.get("/tasks?completed=true", headers=auth_headers)
    assert res.json()["total"] == 1

    res2 = client.get("/tasks?completed=false", headers=auth_headers)
    assert res2.json()["total"] == 1


def test_get_task(client, auth_headers):
    r = client.post("/tasks", json={"title": "Specific"}, headers=auth_headers)
    task_id = r.json()["id"]
    res = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["title"] == "Specific"


def test_get_task_not_found(client, auth_headers):
    res = client.get("/tasks/9999", headers=auth_headers)
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_task(client, auth_headers):
    r = client.post("/tasks", json={"title": "Old title"}, headers=auth_headers)
    task_id = r.json()["id"]
    res = client.put(f"/tasks/{task_id}", json={"title": "New title", "completed": True}, headers=auth_headers)
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["title"] == "New title"
    assert res.json()["completed"] is True


def test_delete_task(client, auth_headers):
    r = client.post("/tasks", json={"title": "To delete"}, headers=auth_headers)
    task_id = r.json()["id"]
    res = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert res.status_code == status.HTTP_204_NO_CONTENT
    res2 = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert res2.status_code == status.HTTP_404_NOT_FOUND


def test_task_isolation(client):
    # Register two users
    client.post("/register", json={"email": "a@a.com", "username": "userA", "password": "passA"})
    client.post("/register", json={"email": "b@b.com", "username": "userB", "password": "passB"})

    token_a = client.post("/login", json={"username": "userA", "password": "passA"}).json()["access_token"]
    token_b = client.post("/login", json={"username": "userB", "password": "passB"}).json()["access_token"]

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    r = client.post("/tasks", json={"title": "A's task"}, headers=headers_a)
    task_id = r.json()["id"]

    # User B cannot see User A's task
    res = client.get(f"/tasks/{task_id}", headers=headers_b)
    assert res.status_code == status.HTTP_404_NOT_FOUND
