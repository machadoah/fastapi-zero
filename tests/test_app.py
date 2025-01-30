from fastapi import status
from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_read_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # arrange (organização)

    response = client.get('/')  # act (ação)

    assert response.status_code == status.HTTP_200_OK  # assert (afirmação)
    assert response.json() == {
        'message': 'Hello, World!'
    }  # assert (afirmação)


def test_read_html_deve_retornar_ok_e_html():
    client = TestClient(app)

    response = client.get('/html')

    assert response.status_code == status.HTTP_200_OK
    assert '<h1>Olá, Mundo!</h1>' in response.text

