from fastapi import status
from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_token_expired_after_time(client, user):
    with freeze_time('2004-05-27 15:30:00'):
        # Gerar o token
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

    assert response.status_code == status.HTTP_200_OK
    token = response.json()['access_token']

    with freeze_time('2004-05-27 16:01:00'):
        # Consumir a rota com o token expirado
        response = client.delete(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_wrong_email(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'wrong_email', 'password': user.clean_password},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
