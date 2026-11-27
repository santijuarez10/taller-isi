def create(client, data):
    return client.post("/api/preguntas", json=data)


def test_post_and_get(client, pregunta_data):
    response = create(client, pregunta_data)

    assert response.status_code == 201
    pregunta_id = response.json["id"]
    saved = client.get(f"/api/preguntas/{pregunta_id}").json
    assert saved["titulo"] == pregunta_data["titulo"]
    assert saved["tags"] == ["python", "web"]


def test_list_reuses_categoria_and_tags(client, pregunta_data):
    assert create(client, pregunta_data).status_code == 201
    assert create(client, pregunta_data).status_code == 201

    assert len(client.get("/api/preguntas").json) == 2


def test_post_invalid(client, pregunta_data):
    response = create(client, pregunta_data | {"autor_id": 999, "tags": 5})

    assert response.status_code == 400
    assert set(response.json["details"]) == {"autor_id", "tags"}


def test_patch(client, pregunta_data):
    pregunta_id = create(client, pregunta_data).json["id"]

    response = client.patch(f"/api/preguntas/{pregunta_id}", json={"tags": ["sql"]})

    assert response.status_code == 200
    assert response.json["tags"] == ["sql"]
    assert response.json["titulo"] == pregunta_data["titulo"]


def test_delete(client, pregunta_data):
    pregunta_id = create(client, pregunta_data).json["id"]

    assert client.delete(f"/api/preguntas/{pregunta_id}").status_code == 204
    assert client.get(f"/api/preguntas/{pregunta_id}").status_code == 404
    assert client.delete(f"/api/preguntas/{pregunta_id}").status_code == 404
