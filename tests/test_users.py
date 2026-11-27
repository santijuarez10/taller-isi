ADA = {"name": "Ada Lovelace", "email": "ada@example.com"}


def test_users_index_empty(client):
    response = client.get("/users/")

    assert response.status_code == 200
    assert b"Listado de usuarios" in response.data


def test_create_user(client):
    response = client.post("/users", data=ADA)

    assert response.status_code == 302
    assert b"Ada Lovelace" in client.get("/users").data


def test_create_user_invalid(client):
    response = client.post("/users", data={"name": " ", "email": "sin-arroba"})

    assert response.status_code == 400


def test_create_user_duplicated_email(client):
    client.post("/users", data=ADA)

    assert client.post("/users", data=ADA).status_code == 409


def test_edit_and_delete_user(client, user_id):
    assert client.get("/users/new").status_code == 200
    assert client.get(f"/users/{user_id}/edit").status_code == 200

    response = client.post(
        f"/users/{user_id}", data={"name": "Ada King", "email": ADA["email"]}
    )
    assert response.status_code == 302
    assert b"Ada King" in client.get(f"/users/{user_id}").data

    assert client.post(f"/users/{user_id}/delete").status_code == 302
    assert client.get(f"/users/{user_id}").status_code == 404
