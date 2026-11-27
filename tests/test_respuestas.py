def crear_pregunta(client, pregunta_data):
    return client.post("/api/preguntas", json=pregunta_data).json["id"]


def crear_usuario(client, name, email):
    return client.post("/api/users", json={"name": name, "email": email}).json["id"]


def test_api_responder_y_listar(client, pregunta_data):
    pregunta_id = crear_pregunta(client, pregunta_data)
    otro_id = crear_usuario(client, "Grace Hopper", "grace@example.com")
    url = f"/api/preguntas/{pregunta_id}/respuestas"

    response = client.post(url, json={"cuerpo": "Agrupa rutas.", "autor_id": otro_id})

    assert response.status_code == 201
    assert response.json["cuerpo"] == "Agrupa rutas."
    assert response.json["autor_id"] == otro_id
    assert response.json["es_aceptada"] is False
    assert [r["id"] for r in client.get(url).json] == [response.json["id"]]


def test_api_validacion(client, pregunta_data):
    pregunta_id = crear_pregunta(client, pregunta_data)
    url = f"/api/preguntas/{pregunta_id}/respuestas"

    response = client.post(url, json={"cuerpo": "", "autor_id": 999})

    assert response.status_code == 400
    assert set(response.json["details"]) == {"cuerpo", "autor_id"}


def test_api_pregunta_inexistente(client, user_id):
    response = client.post(
        "/api/preguntas/999/respuestas", json={"cuerpo": "Hola", "autor_id": user_id}
    )

    assert response.status_code == 404
    assert client.get("/api/preguntas/999/respuestas").status_code == 404


def test_web_responder(client, pregunta_data):
    pregunta_id = crear_pregunta(client, pregunta_data)
    otro_id = crear_usuario(client, "Grace Hopper", "grace@example.com")

    response = client.post(
        f"/preguntas/{pregunta_id}/respuestas",
        data={"cuerpo": "Un Blueprint agrupa rutas.", "autor_id": otro_id},
    )

    assert response.status_code == 302
    page = client.get(f"/preguntas/{pregunta_id}").text
    assert "Un Blueprint agrupa rutas." in page
    assert "Respuestas (1)" in page


def test_web_responder_valida(client, pregunta_data):
    pregunta_id = crear_pregunta(client, pregunta_data)

    response = client.post(f"/preguntas/{pregunta_id}/respuestas", data={"cuerpo": ""})

    assert response.status_code == 400
    assert "Es obligatorio" in response.text


def test_borrar_pregunta_borra_sus_respuestas(client, pregunta_data, user_id):
    pregunta_id = crear_pregunta(client, pregunta_data)
    url = f"/api/preguntas/{pregunta_id}/respuestas"
    client.post(url, json={"cuerpo": "Hola", "autor_id": user_id})

    assert client.delete(f"/api/preguntas/{pregunta_id}").status_code == 204
    assert client.get(url).status_code == 404


def test_no_se_borra_usuario_con_respuestas(client, pregunta_data):
    pregunta_id = crear_pregunta(client, pregunta_data)
    otro_id = crear_usuario(client, "Grace Hopper", "grace@example.com")
    url = f"/api/preguntas/{pregunta_id}/respuestas"
    client.post(url, json={"cuerpo": "Hola", "autor_id": otro_id})

    assert client.delete(f"/api/users/{otro_id}").status_code == 409
