def test_web_crud(client, pregunta_data):
    form = pregunta_data | {"tags": "python, web"}

    assert client.get("/").status_code == 302
    assert client.get("/preguntas/new").status_code == 200

    response = client.post("/preguntas", data=form)
    assert response.status_code == 302
    url = response.headers["Location"]

    assert "Blueprint" in client.get("/preguntas").text
    assert "python" in client.get(url).text
    assert client.get(f"{url}/edit").status_code == 200

    response = client.post(url, data=form | {"titulo": "Título nuevo"})
    assert response.status_code == 302
    assert "Título nuevo" in client.get(url).text

    assert client.post(f"{url}/delete").status_code == 302
    assert client.get(url).status_code == 404


def test_web_validation(client, pregunta_data):
    response = client.post("/preguntas", data={"titulo": ""})

    assert response.status_code == 400
    assert "Es obligatorio" in response.text
