from fastapi import status


def test_read_html_deve_retornar_ok_e_html(client):
    response = client.get('/html')

    assert response.status_code == status.HTTP_200_OK
    assert '<h1>Olá, Mundo!</h1>' in response.text
