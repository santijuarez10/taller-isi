def test_users_index(client):
    response = client.get("/users/")

    assert response.status_code == 200
    assert b"Listado de usuarios" in response.data
    assert b"Ada Lovelace" in response.data
    assert b"Alan Turing" in response.data
