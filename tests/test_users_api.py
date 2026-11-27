ADA = {"name": "Ada Lovelace", "email": "ada@example.com"}


def test_list_users(client, user_id):
    response = client.get("/api/users")

    assert response.status_code == 200
    assert response.json == [{"id": user_id, **ADA}]


def test_get_user(client, user_id):
    assert client.get(f"/api/users/{user_id}").json == {"id": user_id, **ADA}
    assert client.get("/api/users/999").status_code == 404


def test_post_user(client):
    response = client.post("/api/users", json=ADA)

    assert response.status_code == 201
    assert response.headers["Location"].endswith(f"/api/users/{response.json['id']}")


def test_post_user_errors(client, user_id):
    assert client.post("/api/users", json={}).status_code == 400
    assert client.post("/api/users", data="no es json").status_code == 400
    assert client.post("/api/users", json=ADA).status_code == 409


def test_patch_user(client, user_id):
    response = client.patch(f"/api/users/{user_id}", json={"name": "Ada King"})

    assert response.status_code == 200
    assert response.json["name"] == "Ada King"
    assert response.json["email"] == ADA["email"]


def test_delete_user(client, user_id):
    assert client.delete(f"/api/users/{user_id}").status_code == 204
    assert client.get(f"/api/users/{user_id}").status_code == 404


def test_cannot_delete_user_with_preguntas(client, user_id, pregunta_data):
    client.post("/api/preguntas", json=pregunta_data)

    assert client.delete(f"/api/users/{user_id}").status_code == 409
