from fastapi import status
from jwt import decode

from fastapi_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
